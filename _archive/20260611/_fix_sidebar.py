import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'D:\V3.3.3-Core\templates\index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

changes = []

# Fix 1: Logo + home icon (already done in previous run, check if still needed)
old_logo = '''  <div class="sd-logo">
    <div class="sd-logo-m">V3.3.3-Core</div>
    <div class="sd-logo-s">分析系统</div>
  </div>'''
new_logo = '''  <div class="sd-logo">
    <a href="/" class="sd-home" title="返回首页">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
      </svg>
    </a>
    <div>
      <div class="sd-logo-m">V3.3.3-Core</div>
      <div class="sd-logo-s">分析系统</div>
    </div>
  </div>'''
if old_logo in html:
    html = html.replace(old_logo, new_logo); changes.append('Home icon SVG')
else:
    # Already replaced, check if SVG exists
    if '<svg' not in html:
        changes.append('Home icon: already done (skipped)')

# Fix 2: CSS - add logo layout, tooltip, date-item styles
old_body_css = 'body{font-family:var(--sans);background:var(--bg);color:var(--t1);min-height:100vh;display:flex;-webkit-font-smoothing:antialiased}'
new_css_block = '''body{font-family:var(--sans);background:var(--bg);color:var(--t1);min-height:100vh;display:flex;-webkit-font-smoothing:antialiased}
.sd-logo{display:flex;align-items:center;gap:10px;padding:22px 16px 18px;border-bottom:1px solid var(--bd);position:relative}
.sd-home{display:flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:6px;cursor:pointer;transition:background 0.2s;flex-shrink:0}
.sd-home:hover{background:rgba(0,230,118,0.12)}
.sd-home:hover::after{content:attr(title);position:absolute;left:50px;top:50%;transform:translateY(-50%);background:var(--surface-2);color:var(--t2);font-size:11px;padding:4px 10px;border-radius:4px;white-space:nowrap;border:1px solid var(--bd);z-index:10;font-weight:400}
.date-item .d{font-size:13px;font-weight:600}
.date-item.today-item .d{font-size:14px;font-weight:700;color:var(--green)}
.date-item.today-item .s{color:var(--green);font-size:10px}
.date-item.hist-item .d{font-size:12px;font-weight:500;color:var(--t2)}
.date-item.hist-item .s{font-size:10px;color:var(--t3)}
.date-item.hist-item:hover .d{color:var(--t1)}'''
html = html.replace(old_body_css, new_css_block); changes.append('CSS styles added')

# Remove old sd-logo CSS if still exists (should be part of the new block now)
old_sd_logo_css = '.sd-logo{padding:22px 16px 18px;border-bottom:1px solid var(--bd)}'
html = html.replace(old_sd_logo_css, ''); changes.append('Removed old sd-logo CSS')

# Fix 3: Replace the full renderDateList function
# Find function boundaries precisely
func_marker = 'function renderDateList(){'
start = html.find(func_marker)
if start >= 0:
    # Find the matching closing brace - count braces from function start
    end = start + len(func_marker)
    brace_count = 1
    while end < len(html) and brace_count > 0:
        if html[end] == '{':
            brace_count += 1
        elif html[end] == '}':
            brace_count -= 1
        end += 1
    
    old_func = html[start:end]
    print('Found renderDateList at %d, length %d, end at %d' % (start, len(old_func), end))
    
    new_func = '''function renderDateList(){
  var el=document.getElementById("historyDateList");
  var h="";
  // Determine "today" from the most recent run
  var todayStr = "";
  if(HISTORY_RUNS && HISTORY_RUNS.length>0){
    var sorted = HISTORY_RUNS.slice().sort(function(a,b){
      var da = a.prediction_date||a.date||"";
      var db = b.prediction_date||b.date||"";
      return da > db ? -1 : da < db ? 1 : 0;
    });
    todayStr = sorted[0].prediction_date||sorted[0].date||"";
  }
  var currentIsToday = !CURRENT_DATE || CURRENT_DATE === todayStr;
  // "今日扫盘" - always first, highlighted
  h+='<li class="date-item today-item'+(currentIsToday?' active':'')+'" data-date="today">';
  h+='<div class="d">今日扫盘</div>';
  h+='<div class="s">'+(todayStr||'最新预测')+'</div>';
  h+='</li>';
  // Build historical date list (deduplicated, filtered, sorted desc)
  if(HISTORY_RUNS && HISTORY_RUNS.length>0){
    var seen = {};
    var sorted = HISTORY_RUNS.slice().sort(function(a,b){
      var da = a.prediction_date||a.date||"";
      var db = b.prediction_date||b.date||"";
      return da > db ? -1 : da < db ? 1 : 0;
    });
    sorted.forEach(function(r){
      var d = r.prediction_date||r.date||"";
      if(!d || d === todayStr) return;
      if(seen[d]) return;
      seen[d] = true;
      var active = (d===CURRENT_DATE)?" active":"";
      var total = r.total_matches||0;
      var hit = r.hit_count||0;
      var rate = total>0?Math.round(hit/total*100):0;
      var statStr = total+"场 "+hit+"胜 "+rate+"%";
      h+='<li class="date-item hist-item'+active+'" data-date="'+d+'">';
      h+='<div class="d">'+d+'</div>';
      h+='<div class="s">'+(statStr||"")+'</div>';
      h+='</li>';
    });
  } else {
    // Fallback demo data
    var demoDates=["2026-06-05","2026-06-04","2026-06-03","2026-06-02","2026-06-01"];
    demoDates.forEach(function(d){
      h+='<li class="date-item hist-item" data-date="'+d+'">';
      h+='<div class="d">'+d+'</div>';
      h+='<div class="s">点击查看</div>';
      h+='</li>';
    });
  }
  el.innerHTML=h;
  el.querySelectorAll(".date-item").forEach(function(item){
    item.addEventListener("click",function(){
      var date=this.getAttribute("data-date");
      if(!date) return;
      if(date==="today"){
        loadToday();
        el.querySelectorAll(".date-item").forEach(function(x){x.classList.remove("active");});
        this.classList.add("active");
        return;
      }
      CURRENT_DATE=date;
      el.querySelectorAll(".date-item").forEach(function(x){x.classList.remove("active");});
      this.classList.add("active");
      document.querySelector(".sec-header h2").textContent="历史扫盘 - "+date;
      document.getElementById("todayMatches").style.display="none";
      document.getElementById("yesterdayContent").style.display="block";
      loadYesterday(date);
    });
  });
}'''
    html = html.replace(old_func, new_func); changes.append('renderDateList function replaced')
else:
    changes.append('ERROR: renderDateList not found')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print()
print('Changes applied: %d' % len(changes))
for c in changes:
    print('  -', c)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    h = f.read()
v = [
    ('SVG home icon', 'sd-home' in h),
    ('Tooltip title', '返回首页' in h),
    ('today-item class', 'today-item' in h),
    ('hist-item class', 'hist-item' in h),
    ('Deduplication', 'seen[d]' in h),
    ('Filter today from history', 'd === todayStr' in h),
    ('Sort descending', 'da > db ? -1' in h),
    ('No sort toggle button', '排序' not in h and 'toggle' not in h),
]
print()
for name, ok in v:
    print('  [%s] %s' % ('OK' if ok else 'FAIL', name))
