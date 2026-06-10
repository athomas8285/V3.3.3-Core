import sys
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()
changes = []

# ── 1. Rename sidebar "今日赛程" → "小组赛程" ──
html = html.replace("\u4eca\u65e5\u8d5b\u7a0b", "\u5c0f\u7ec4\u8d5b\u7a0b")
changes.append('Rename sidebar item to "小组赛程"')

# ── 2. Change onclick from #today to render function ──
html = html.replace(
    'onclick="location.href=\'#today\'"',
    'onclick="return renderGroupSchedule()"',
)
changes.append("Change sidebar onclick to renderGroupSchedule()")

# ── 3. Embed 72 matches data ──
# Build the JS data array - I will insert it before </script>
match_data = """// 2026 \u4e16\u754c\u676f \u5c0f\u7ec4\u8d5b 72\u573a\u5bf9\u9635
var WC_MATCHES = [
  // \u0036\u6708\u0031\u0032\u65e5
  {d:"\u0036\u6708\u0031\u0032\u65e5",t:"03:00",g:"A",h:"\u58a8\u897f\u54e5",a:"\u5357\u975e",v:"\u58a8\u897f\u54e5\u57ce"},
  {d:"\u0036\u6708\u0031\u0032\u65e5",t:"10:00",g:"A",h:"\u97e9\u56fd",a:"\u6377\u514b",v:"\u74dc\u8fbe\u62c9\u54c8\u62c9"},
  // \u0036\u6708\u0031\u0033\u65e5
  {d:"\u0036\u6708\u0031\u0033\u65e5",t:"03:00",g:"B",h:"\u52a0\u62ff\u5927",a:"\u6ce2\u9ed1",v:"\u591a\u4f26\u591a"},
  {d:"\u0036\u6708\u0031\u0033\u65e5",t:"09:00",g:"D",h:"\u7f8e\u56fd",a:"\u5df4\u62c9\u572d",v:"\u6d1b\u6749\u77f6"},
  // \u0036\u6708\u0031\u0034\u65e5
  {d:"\u0036\u6708\u0031\u0034\u65e5",t:"03:00",g:"B",h:"\u5361\u5854\u5c14",a:"\u745e\u58eb",v:"\u65e7\u91d1\u5c71\u6e7e\u533a"},
  {d:"\u0036\u6708\u0031\u0034\u65e5",t:"06:00",g:"C",h:"\u5df4\u897f",a:"\u6469\u6d1b\u54e5",v:"\u7ebd\u7ea6/\u65b0\u6cfd\u897f"},
  {d:"\u0036\u6708\u0031\u0034\u65e5",t:"09:00",g:"C",h:"\u6d77\u5730",a:"\u82cf\u683c\u5170",v:"\u6ce2\u58eb\u987f"},
  {d:"\u0036\u6708\u0031\u0034\u65e5",t:"12:00",g:"D",h:"\u5965\u5927\u5229\u4e9a",a:"\u571f\u8033\u5176",v:"\u6e29\u54e5\u534e"},
  // \u0036\u6708\u0031\u0035\u65e5
  {d:"\u0036\u6708\u0031\u0035\u65e5",t:"01:00",g:"E",h:"\u5fb7\u56fd",a:"\u5e93\u62c9\u7d22",v:"\u4f11\u65af\u6566"},
  {d:"\u0036\u6708\u0031\u0035\u65e5",t:"04:00",g:"F",h:"\u8377\u5170",a:"\u65e5\u672c",v:"\u8fbe\u62c9\u65af"},
  {d:"\u0036\u6708\u0031\u0035\u65e5",t:"07:00",g:"E",h:"\u79d1\u7279\u8fea\u74e6",a:"\u5384\u74dc\u591a\u5c14",v:"\u8d39\u57ce"},
  {d:"\u0036\u6708\u0031\u0035\u65e5",t:"10:00",g:"F",h:"\u745e\u5178",a:"\u7a81\u5c3c\u65af",v:"\u8499\u7279\u96f7"},
  // \u0036\u6708\u0031\u0036\u65e5
  {d:"\u0036\u6708\u0031\u0036\u65e5",t:"00:00",g:"H",h:"\u897f\u73ed\u7259",a:"\u4f5b\u5f97\u89d2",v:"\u4e9a\u7279\u5170\u5927"},
  {d:"\u0036\u6708\u0031\u0036\u65e5",t:"03:00",g:"G",h:"\u6bd4\u5229\u65f6",a:"\u57c3\u53ca",v:"\u897f\u96c5\u56fe"},
  {d:"\u0036\u6708\u0031\u0036\u65e5",t:"06:00",g:"H",h:"\u6c99\u7279",a:"\u4e4c\u62c9\u572d",v:"\u8fc8\u963f\u5bc6"},
  {d:"\u0036\u6708\u0031\u0036\u65e5",t:"09:00",g:"G",h:"\u4f0a\u6717",a:"\u65b0\u897f\u5170",v:"\u6d1b\u6749\u77f6"},
  // \u0036\u6708\u0031\u0037\u65e5
  {d:"\u0036\u6708\u0031\u0037\u65e5",t:"03:00",g:"I",h:"\u6cd5\u56fd",a:"\u585e\u5185\u52a0\u5c14",v:"\u7ebd\u7ea6/\u65b0\u6cfd\u897f"},
  {d:"\u0036\u6708\u0031\u0037\u65e5",t:"06:00",g:"I",h:"\u4f0a\u62c9\u514b",a:"\u632a\u5a01",v:"\u6ce2\u58eb\u987f"},
  {d:"\u0036\u6708\u0031\u0037\u65e5",t:"09:00",g:"J",h:"\u963f\u6839\u5ef7",a:"\u963f\u5c14\u53ca\u5229\u4e9a",v:"\u582a\u8428\u65af\u57ce"},
  {d:"\u0036\u6708\u0031\u0037\u65e5",t:"12:00",g:"J",h:"\u5965\u5730\u5229",a:"\u7ea6\u65e6",v:"\u65e7\u91d1\u5c71\u6e7e\u533a"},
  // \u0036\u6708\u0031\u0038\u65e5
  {d:"\u0036\u6708\u0031\u0038\u65e5",t:"01:00",g:"K",h:"\u8461\u8404\u7259",a:"\u6c11\u4e3b\u521a\u679c",v:"\u4f11\u65af\u6566"},
  {d:"\u0036\u6708\u0031\u0038\u65e5",t:"04:00",g:"L",h:"\u82f1\u683c\u5170",a:"\u514b\u7f57\u5730\u4e9a",v:"\u8fbe\u62c9\u65af"},
  {d:"\u0036\u6708\u0031\u0038\u65e5",t:"07:00",g:"L",h:"\u52a0\u7eb3",a:"\u5df4\u62ff\u9a6c",v:"\u591a\u4f26\u591a"},
  {d:"\u0036\u6708\u0031\u0038\u65e5",t:"10:00",g:"K",h:"\u4e4c\u5179\u522b\u514b\u65af\u5766",a:"\u54e5\u4f26\u6bd4\u4e9a",v:"\u58a8\u897f\u54e5\u57ce"},
  // \u0036\u6708\u0031\u0039\u65e5
  {d:"\u0036\u6708\u0031\u0039\u65e5",t:"00:00",g:"A",h:"\u6377\u514b",a:"\u5357\u975e",v:"\u4e9a\u7279\u5170\u5927"},
  {d:"\u0036\u6708\u0031\u0039\u65e5",t:"03:00",g:"B",h:"\u745e\u58eb",a:"\u6ce2\u9ed1",v:"\u6d1b\u6749\u77f6"},
  {d:"\u0036\u6708\u0031\u0039\u65e5",t:"06:00",g:"B",h:"\u52a0\u62ff\u5927",a:"\u5361\u5854\u5c14",v:"\u6e29\u54e5\u534e"},
  {d:"\u0036\u6708\u0031\u0039\u65e5",t:"09:00",g:"A",h:"\u58a8\u897f\u54e5",a:"\u97e9\u56fd",v:"\u74dc\u8fbe\u62c9\u54c8\u62c9"},
  // \u0036\u6708\u0032\u0030\u65e5
  {d:"\u0036\u6708\u0032\u0030\u65e5",t:"03:00",g:"D",h:"\u7f8e\u56fd",a:"\u5965\u5927\u5229\u4e9a",v:"\u897f\u96c5\u56fe"},
  {d:"\u0036\u6708\u0032\u0030\u65e5",t:"06:00",g:"C",h:"\u82cf\u683c\u5170",a:"\u6469\u6d1b\u54e5",v:"\u6ce2\u58eb\u987f"},
  {d:"\u0036\u6708\u0032\u0030\u65e5",t:"09:00",g:"C",h:"\u5df4\u897f",a:"\u6d77\u5730",v:"\u8d39\u57ce"},
  {d:"\u0036\u6708\u0032\u0030\u65e5",t:"12:00",g:"D",h:"\u571f\u8033\u5176",a:"\u5df4\u62c9\u572d",v:"\u8499\u7279\u96f7"},
  // \u0036\u6708\u0032\u0031\u65e5
  {d:"\u0036\u6708\u0032\u0031\u65e5",t:"01:00",g:"F",h:"\u8377\u5170",a:"\u745e\u5178",v:"\u4f11\u65af\u6566"},
  {d:"\u0036\u6708\u0032\u0031\u65e5",t:"04:00",g:"E",h:"\u5fb7\u56fd",a:"\u79d1\u7279\u8fea\u74e6",v:"\u591a\u4f26\u591a"},
  {d:"\u0036\u6708\u0032\u0031\u65e5",t:"08:00",g:"E",h:"\u5384\u74dc\u591a\u5c14",a:"\u5e93\u62c9\u7d22",v:"\u582a\u8428\u65af\u57ce"},
  {d:"\u0036\u6708\u0032\u0031\u65e5",t:"12:00",g:"F",h:"\u7a81\u5c3c\u65af",a:"\u65e5\u672c",v:"\u8499\u7279\u96f7"},
  // \u0036\u6708\u0032\u0032\u65e5
  {d:"\u0036\u6708\u0032\u0032\u65e5",t:"00:00",g:"H",h:"\u897f\u73ed\u7259",a:"\u6c99\u7279",v:"\u4e9a\u7279\u5170\u5927"},
  {d:"\u0036\u6708\u0032\u0032\u65e5",t:"03:00",g:"G",h:"\u6bd4\u5229\u65f6",a:"\u4f0a\u6717",v:"\u6d1b\u6749\u77f6"},
  {d:"\u0036\u6708\u0032\u0032\u65e5",t:"06:00",g:"H",h:"\u4e4c\u62c9\u572d",a:"\u4f5b\u5f97\u89d2",v:"\u8fc8\u963f\u5bc6"},
  {d:"\u0036\u6708\u0032\u0032\u65e5",t:"09:00",g:"G",h:"\u65b0\u897f\u5170",a:"\u57c3\u53ca",v:"\u6e29\u54e5\u534e"},
  // \u0036\u6708\u0032\u0033\u65e5
  {d:"\u0036\u6708\u0032\u0033\u65e5",t:"01:00",g:"J",h:"\u963f\u6839\u5ef7",a:"\u5965\u5730\u5229",v:"\u8fbe\u62c9\u65af"},
  {d:"\u0036\u6708\u0032\u0033\u65e5",t:"05:00",g:"I",h:"\u6cd5\u56fd",a:"\u4f0a\u62c9\u514b",v:"\u8d39\u57ce"},
  {d:"\u0036\u6708\u0032\u0033\u65e5",t:"08:00",g:"I",h:"\u632a\u5a01",a:"\u585e\u5185\u52a0\u5c14",v:"\u7ebd\u7ea6/\u65b0\u6cfd\u897f"},
  {d:"\u0036\u6708\u0032\u0033\u65e5",t:"11:00",g:"J",h:"\u7ea6\u65e6",a:"\u963f\u5c14\u53ca\u5229\u4e9a",v:"\u582a\u8428\u65af\u57ce"},
  // \u0036\u6708\u0032\u0034\u65e5
  {d:"\u0036\u6708\u0032\u0034\u65e5",t:"01:00",g:"K",h:"\u8461\u8404\u7259",a:"\u4e4c\u5179\u522b\u514b\u65af\u5766",v:"\u4f11\u65af\u6566"},
  {d:"\u0036\u6708\u0032\u0034\u65e5",t:"04:00",g:"L",h:"\u82f1\u683c\u5170",a:"\u52a0\u7eb3",v:"\u6ce2\u58eb\u987f"},
  {d:"\u0036\u6708\u0032\u0034\u65e5",t:"07:00",g:"L",h:"\u5df4\u62ff\u9a6c",a:"\u514b\u7f57\u5730\u4e9a",v:"\u591a\u4f26\u591a"},
  {d:"\u0036\u6708\u0032\u0034\u65e5",t:"10:00",g:"K",h:"\u54e5\u4f26\u6bd4\u4e9a",a:"\u6c11\u4e3b\u521a\u679c",v:"\u58a8\u897f\u54e5\u57ce"},
  // \u0036\u6708\u0032\u0035\u65e5
  {d:"\u0036\u6708\u0032\u0035\u65e5",t:"03:00",g:"B",h:"\u745e\u58eb",a:"\u52a0\u62ff\u5927",v:"\u6e29\u54e5\u534e"},
  {d:"\u0036\u6708\u0032\u0035\u65e5",t:"03:00",g:"B",h:"\u6ce2\u9ed1",a:"\u5361\u5854\u5c14",v:"\u897f\u96c5\u56fe"},
  {d:"\u0036\u6708\u0032\u0035\u65e5",t:"06:00",g:"C",h:"\u82cf\u683c\u5170",a:"\u5df4\u897f",v:"\u8fc8\u963f\u5bc6"},
  {d:"\u0036\u6708\u0032\u0035\u65e5",t:"06:00",g:"C",h:"\u6469\u6d1b\u54e5",a:"\u6d77\u5730",v:"\u4e9a\u7279\u5170\u5927"},
  {d:"\u0036\u6708\u0032\u0035\u65e5",t:"09:00",g:"A",h:"\u6377\u514b",a:"\u58a8\u897f\u54e5",v:"\u58a8\u897f\u54e5\u57ce"},
  {d:"\u0036\u6708\u0032\u0035\u65e5",t:"09:00",g:"A",h:"\u5357\u975e",a:"\u97e9\u56fd",v:"\u8499\u7279\u96f7"},
  // \u0036\u6708\u0032\u0036\u65e5
  {d:"\u0036\u6708\u0032\u0036\u65e5",t:"04:00",g:"E",h:"\u5384\u74dc\u591a\u5c14",a:"\u5fb7\u56fd",v:"\u7ebd\u7ea6/\u65b0\u6cfd\u897f"},
  {d:"\u0036\u6708\u0032\u0036\u65e5",t:"04:00",g:"E",h:"\u5e93\u62c9\u7d22",a:"\u79d1\u7279\u8fea\u74e6",v:"\u8d39\u57ce"},
  {d:"\u0036\u6708\u0032\u0036\u65e5",t:"07:00",g:"F",h:"\u65e5\u672c",a:"\u745e\u5178",v:"\u8fbe\u62c9\u65af"},
  {d:"\u0036\u6708\u0032\u0036\u65e5",t:"07:00",g:"F",h:"\u7a81\u5c3c\u65af",a:"\u8377\u5170",v:"\u582a\u8428\u65af\u57ce"},
  {d:"\u0036\u6708\u0032\u0036\u65e5",t:"10:00",g:"D",h:"\u571f\u8033\u5176",a:"\u7f8e\u56fd",v:"\u6d1b\u6749\u77f6"},
  {d:"\u0036\u6708\u0032\u0036\u65e5",t:"10:00",g:"D",h:"\u5df4\u62c9\u572d",a:"\u5965\u5927\u5229\u4e9a",v:"\u65e7\u91d1\u5c71\u6e7e\u533a"},
  // \u0036\u6708\u0032\u0037\u65e5
  {d:"\u0036\u6708\u0032\u0037\u65e5",t:"03:00",g:"I",h:"\u632a\u5a01",a:"\u6cd5\u56fd",v:"\u6ce2\u58eb\u987f"},
  {d:"\u0036\u6708\u0032\u0037\u65e5",t:"03:00",g:"I",h:"\u585e\u5185\u52a0\u5c14",a:"\u4f0a\u62c9\u514b",v:"\u8d39\u57ce"},
  {d:"\u0036\u6708\u0032\u0037\u65e5",t:"08:00",g:"H",h:"\u4f5b\u5f97\u89d2",a:"\u6c99\u7279",v:"\u4e9a\u7279\u5170\u5927"},
  {d:"\u0036\u6708\u0032\u0037\u65e5",t:"08:00",g:"H",h:"\u4e4c\u62c9\u572d",a:"\u897f\u73ed\u7259",v:"\u8fc8\u963f\u5bc6"},
  {d:"\u0036\u6708\u0032\u0037\u65e5",t:"11:00",g:"G",h:"\u57c3\u53ca",a:"\u4f0a\u6717",v:"\u897f\u96c5\u56fe"},
  {d:"\u0036\u6708\u0032\u0037\u65e5",t:"11:00",g:"G",h:"\u65b0\u897f\u5170",a:"\u6bd4\u5229\u65f6",v:"\u6e29\u54e5\u534e"},
  // \u0036\u6708\u0032\u0038\u65e5
  {d:"\u0036\u6708\u0032\u0038\u65e5",t:"03:00",g:"L",h:"\u5df4\u62ff\u9a6c",a:"\u82f1\u683c\u5170",v:"\u7ebd\u7ea6/\u65b0\u6cfd\u897f"},
  {d:"\u0036\u6708\u0032\u0038\u65e5",t:"03:00",g:"L",h:"\u514b\u7f57\u5730\u4e9a",a:"\u52a0\u7eb3",v:"\u8d39\u57ce"},
  {d:"\u0036\u6708\u0032\u0038\u65e5",t:"07:30",g:"K",h:"\u54e5\u4f26\u6bd4\u4e9a",a:"\u8461\u8404\u7259",v:"\u8fc8\u963f\u5bc6"},
  {d:"\u0036\u6708\u0032\u0038\u65e5",t:"07:30",g:"K",h:"\u6c11\u4e3b\u521a\u679c",a:"\u4e4c\u5179\u522b\u514b\u65af\u5766",v:"\u4e9a\u7279\u5170\u5927"},
  {d:"\u0036\u6708\u0032\u0038\u65e5",t:"10:00",g:"J",h:"\u963f\u5c14\u53ca\u5229\u4e9a",a:"\u5965\u5730\u5229",v:"\u582a\u8428\u65af\u57ce"},
  {d:"\u0036\u6708\u0032\u0038\u65e5",t:"10:00",g:"J",h:"\u7ea6\u65e6",a:"\u963f\u6839\u5ef7",v:"\u65e7\u91d1\u5c71\u6e7e\u533a"},
];"""

# Also need to add the render function and CSS
render_func = """
// \u6e32\u67d3\u5c0f\u7ec4\u8d5b\u7a0b
function renderGroupSchedule(){
  var main = document.querySelector(".main");
  main.scrollTop = 0;
  // Update header
  document.querySelector(".sec-header h2").textContent = "\u5c0f\u7ec4\u8d5b\u7a0b";
  document.getElementById("todaySub").textContent = "72\u573a \u5c0f\u7ec4\u8d5b A-L\u7ec4";
  document.getElementById("todayMatches").style.display = "block";
  document.getElementById("yesterdayContent").style.display = "none";
  // Build HTML
  var h = \'\';
  var curDate = \'\';
  for(var i = 0; i < WC_MATCHES.length; i++){
    var m = WC_MATCHES[i];
    if(m.d !== curDate){
      if(curDate !== \'\') h += \'</div>\';
      curDate = m.d;
      h += \'<div class="wc-date-group">\';
      h += \'<div class="wc-date-head">\' + curDate + \'</div>\';
    }
    h += \'<div class="wc-match-card" onclick="alert(\'+\'\\\'\' + m.h + \' vs \' + m.a + \'\\\'\'+\')\">\';
    h += \'<span class="wc-m-time">\' + m.t + \'</span>\';
    h += \'<span class="wc-m-group">[\' + m.g + \'\u7ec4]</span>\';
    h += \'<span class="wc-m-home">\' + m.h + \'</span>\';
    h += \'<span class="wc-m-vs">vs</span>\';
    h += \'<span class="wc-m-away">\' + m.a + \'</span>\';
    h += \'<span class="wc-m-venue">\' + m.v + \'</span>\';
    h += \'</div>\';
  }
  if(curDate !== \'\') h += \'</div>\';
  document.getElementById("todayMatches").innerHTML = h;
  return false;
}"""

# Find insertion point for match data - before the first usage
script_marker = "if(typeof __DATA"
insert_point = html.find(script_marker)
if insert_point >= 0:
    # Insert data + render function before the DOMContentLoaded logic
    html = html[:insert_point] + match_data + "\n" + render_func + "\n\n" + html[insert_point:]
    changes.append("Embed 72 match data + render function")

# ── 4. Change default page load ──
# Replace the initial load logic to call renderGroupSchedule instead of loadToday
old_init = 'openAccordion("accWCMain");\n  if(typeof __DATA!=="undefined"&&__DATA&&__DATA.rating&&__DATA.rating.length>0){renderToday(__DATA.rating);document.getElementById("todaySub").textContent="2026-06-06 | "+__DATA.rating.length+"\u573a";updateTodayOverview({matches:__DATA.rating,date:"2026-06-06"});}else{loadToday();}'
new_init = 'openAccordion("accWCMain");\n  renderGroupSchedule();'
if old_init in html:
    html = html.replace(old_init, new_init)
    changes.append("Change default page load to renderGroupSchedule")

# ── 5. Add WC schedule CSS ──
wc_schedule_css = """
/* WC group schedule */
.wc-date-group{margin-bottom:12px}
.wc-date-head{font-size:15px;font-weight:700;color:var(--gold);padding:12px 0 6px;border-bottom:1px solid rgba(251,191,36,.12);margin-bottom:8px;letter-spacing:.5px;text-shadow:0 0 8px rgba(251,191,36,.1)}
.wc-match-card{display:flex;align-items:center;gap:10px;padding:9px 14px;margin:4px 0;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.04);border-radius:6px;cursor:pointer;transition:all .15s;font-size:13px}
.wc-match-card:hover{background:rgba(251,191,36,.04);border-color:rgba(251,191,36,.1)}
.wc-m-time{font-family:var(--mono);font-size:12px;color:var(--t3);width:44px;flex-shrink:0;text-align:center}
.wc-m-group{font-size:10px;color:var(--gold);background:rgba(251,191,36,.1);padding:1px 5px;border-radius:3px;flex-shrink:0}
.wc-m-home{flex:1;text-align:right;font-weight:600;color:var(--t1)}
.wc-m-vs{color:var(--t3);font-size:11px;flex-shrink:0;width:20px;text-align:center}
.wc-m-away{flex:1;font-weight:600;color:var(--t1)}
.wc-m-venue{font-size:10px;color:var(--t3);flex-shrink:0;max-width:70px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
"""
# Insert before .sd-footer CSS
needle = ".sd-footer{padding:10px 16px;font-size:9px"
if needle in html:
    html = html.replace(needle, wc_schedule_css.strip() + "\n\n" + needle)
    changes.append("Add WC schedule CSS")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Changes: {len(changes)}")
for c in changes:
    print(f"  - {c}")
