import sys
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()
changes = []

# 1. Add --gold to :root
old_root = ":root{--bg:#080b14;--surface:#0c1021;--surface-2:#111629;--surface-h:#171d35;--t1:#e8edf5;--t2:#8b95a9;--t3:#5a6577;--green:#00e676;--red:#ef5350;--amber:#fbbf24;--blue:#60a5fa;--cyan:#00e5ff;--purple:#7c3aed;--bd:rgba(0,229,255,.06);--bd-h:rgba(0,229,255,.14);--glow-cyan:0 0 12px rgba(0,229,255,.12);--glow-green:0 0 12px rgba(0,230,118,.12);--glow-amber:0 0 12px rgba(251,191,36,.12);--glow-purple:0 0 12px rgba(124,58,237,.12);--mono:\"SF Mono\",\"Cascadia Code\",\"JetBrains Mono\",\"Consolas\",monospace;--sans:\"Inter\",\"SF Pro\",\"Microsoft YaHei\",\"PingFang SC\",\"Noto Sans SC\",sans-serif}"
new_root = ":root{--bg:#080b14;--surface:#0c1021;--surface-2:#111629;--surface-h:#171d35;--t1:#e8edf5;--t2:#8b95a9;--t3:#5a6577;--green:#00e676;--red:#ef5350;--gold:#fbbf24;--amber:#fbbf24;--blue:#60a5fa;--cyan:#00e5ff;--purple:#7c3aed;--bd:rgba(0,229,255,.06);--bd-h:rgba(0,229,255,.14);--glow-cyan:0 0 12px rgba(0,229,255,.12);--glow-green:0 0 12px rgba(0,230,118,.12);--glow-amber:0 0 12px rgba(251,191,36,.12);--glow-gold:0 0 12px rgba(251,191,36,.15);--glow-purple:0 0 12px rgba(124,58,237,.12);--mono:\"SF Mono\",\"Cascadia Code\",\"JetBrains Mono\",\"Consolas\",monospace;--sans:\"Inter\",\"SF Pro\",\"Microsoft YaHei\",\"PingFang SC\",\"Noto Sans SC\",sans-serif}"
if old_root in html:
    html = html.replace(old_root, new_root)
    changes.append("Add --gold CSS variable")

# 2. Replace sd-top header with WC banner
s1 = html.find('<div class="sd-top">')
s2 = html.find('<div class="sd-body">', s1)
if s1 >= 0 and s2 > s1:
    old_top = html[s1:s2]
    new_top = '''  <div class="sd-top">
    <div class="sd-logo-row" style="cursor:pointer" onclick="window.location.href=\'/\'">
      <div class="sd-home" title="\u8fd4\u56de\u9996\u9875">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--gold)">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
          <polyline points="9 22 9 12 15 12 15 22"/>
        </svg>
      </div>
      <div class="sd-title-group">
        <span class="sd-title" style="color:var(--gold)">V3.3.3-Core</span>
        <span class="sd-wc-badge">2026 \u4e16\u754c\u676f\u7248</span>
      </div>
    </div>
    <div class="sd-status">
      <span class="sd-status-dot db-connected"></span>
      <span>\u7cfb\u7edf\u8fd0\u884c\u4e2d</span>
      <span style="color:rgba(255,255,255,.7);margin-left:auto;font-size:10px;white-space:nowrap"><span style="font-weight:300;color:var(--gold);font-size:9px">\u4e16\u754c\u676f</span> v3.3.3</span>
    </div>
  </div>'''
    html = html.replace(old_top, new_top)
    changes.append("Replace sd-top with WC banner")

# 3. Replace accToday+accPlan with accWCMain
s3 = html.find('id="accToday"')
s4 = html.find('id="accHistory"', s3)
if s3 >= 0 and s4 > s3:
    # find the actual div boundaries
    start_marker = '<div class="acc open"'
    end_marker = '<div class="acc" id="accHistory">'
    ss = html.find(start_marker)
    se = html.find(end_marker, ss)
    if ss >= 0 and se > ss:
        old_wc = html[ss:se]
        new_wc = '''    <div class="acc open" id="accWCMain">
      <div class="acc-head" onclick="toggleAccordion(\'accWCMain\')" style="background:linear-gradient(90deg,rgba(251,191,36,.08),transparent 60%)">
        <span class="acc-arrow">\u25b6</span>
        <span class="acc-icon">\U0001f3c6</span>
        <span class="acc-label" style="color:var(--gold);font-weight:700">2026 \u4e16\u754c\u676f\u5206\u6790</span>
        <span class="acc-badge" style="background:rgba(251,191,36,.18);color:var(--gold)">\u706b\u70ed</span>
      </div>
      <div class="acc-body">
        <div class="acc-body-inner" style="padding:4px 12px 10px">
          <div class="wc-sub-item" onclick="location.href=\'#today\'">
            <span class="wsi-icon">\U0001f4c5</span>
            <span class="wsi-label">\u4eca\u65e5\u8d5b\u7a0b</span>
          </div>
          <div class="wc-sub-item" onclick="location.href=\'#standings\'">
            <span class="wsi-icon">\U0001f4ca</span>
            <span class="wsi-label">\u5c0f\u7ec4\u79ef\u5206\u699c</span>
          </div>
          <div class="wc-sub-item" onclick="location.href=\'#bracket\'">
            <span class="wsi-icon">\U0001f3df\ufe0f</span>
            <span class="wsi-label">\u6dd8\u6c70\u8d5b\u5bf9\u9635\u56fe</span>
          </div>
          <div class="wc-sub-item" onclick="location.href=\'#odds\'">
            <span class="wsi-icon">\U0001f4b0</span>
            <span class="wsi-label">\u51a0\u519b\u8d54\u7387\u8ffd\u8e2a</span>
          </div>
          <div class="wc-sub-item" onclick="location.href=\'#top\'">
            <span class="wsi-icon">\u2b50</span>
            <span class="wsi-label">\u4eca\u65e5\u7cbe\u9009\u63a8\u8350</span>
          </div>
        </div>
      </div>
    </div>'''
        html = html.replace(old_wc, new_wc)
        changes.append("Replace accToday+accPlan with accWCMain")

# 4. Remove old WC CSS refs
for old,desc in [('#accWC .acc-head .acc-label{color:var(--gold)}', 'old #accWC.label'), ('#accWC.open>.acc-head{background:linear-gradient(90deg,rgba(251,191,36,.08),transparent 60%)}', 'old #accWC.head'), ('#accWC.open>.acc-head .acc-label{color:var(--gold)}', 'old #accWC.open')]:
    if old in html:
        html = html.replace(old, '')
        changes.append(f"Remove {desc}")

# 5. Insert WC CSS
wc_css = '''
/* WC sidebar */
#accWCMain .acc-head{border-radius:6px;margin:4px 8px}
#accWCMain.open>.acc-head .acc-label{color:var(--gold);text-shadow:0 0 12px rgba(251,191,36,.15)}
.wc-sub-item{display:flex;align-items:center;gap:10px;padding:9px 12px;margin:3px 8px;border-radius:6px;cursor:pointer;transition:all .15s;font-size:13px;color:var(--t2)}
.wc-sub-item:hover{background:rgba(251,191,36,.06);color:var(--t1)}
.wc-sub-item .wsi-icon{font-size:15px;flex-shrink:0}
.wc-sub-item .wsi-label{flex:1}
.sd-wc-badge{font-size:9px;color:var(--gold);background:rgba(251,191,36,.14);padding:1px 7px;border-radius:8px;letter-spacing:.3px;white-space:nowrap}
#accHistory,#accBacktest,#accDoc{opacity:.7;transition:opacity .2s}
#accHistory:hover,#accBacktest:hover,#accDoc:hover{opacity:1}
'''
marker = '.sd-wc-divider{height:1px;margin:8px 18px;background:linear-gradient(90deg,rgba(251,191,36,.12),transparent 60%)}'
if marker in html:
    html = html.replace(marker, marker + '\n' + wc_css.strip())
    changes.append("Add WC sidebar CSS")

# 6. Fix bg1.png path
if "url('/static/bg1.png')" in html:
    html = html.replace("url('/static/bg1.png')", "url('../static/bg1.png')")
    changes.append("Fix bg1.png path")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Changes: {len(changes)}")
for c in changes:
    print(f"  - {c}")
