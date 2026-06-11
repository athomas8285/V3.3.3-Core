import sys

# Read original
with open("D:/V3.3.3-Core/templates/index.html","r",encoding="utf-8-sig") as f:
    c = f.read()

print("Read", len(c), "bytes")

# 1. Add --gold to CSS
c = c.replace("--amber:#fbbf24", "--gold:#fbbf24;--amber:#fbbf24")

# 2. Insert WC CSS
wc_css_idx = c.find(".acc{border-bottom:1px solid transparent;")
wc_css = """/* World Cup gold accent */
.wc-gold{color:var(--gold)}
.wc-badge{font-size:10px;color:var(--gold);background:rgba(251,191,36,.12);padding:2px 8px;border-radius:8px;white-space:nowrap}
#accWC .acc-head .acc-label{color:var(--gold)}
#accWC.open>.acc-head{background:linear-gradient(90deg,rgba(251,191,36,.08),transparent 60%)}
#accWC.open>.acc-head .acc-label{color:var(--gold)}
.wc-sub-item{display:flex;align-items:center;gap:10px;padding:9px 12px;margin:3px 8px;border-radius:6px;cursor:pointer;transition:all .15s;font-size:13px;color:var(--t2)}
.wc-sub-item:hover{background:rgba(251,191,36,.06);color:var(--t1)}
.wc-sub-item.active{color:var(--gold);background:rgba(251,191,36,.08)}
.wc-sub-item .wsi-icon{font-size:15px;flex-shrink:0}
.wc-sub-item .wsi-label{flex:1}
.wc-banner{display:none;background:linear-gradient(135deg,rgba(251,191,36,.06),rgba(251,191,36,.02) 60%,transparent);border:1px solid rgba(251,191,36,.12);border-radius:8px;padding:12px 18px;margin-bottom:16px;align-items:center;gap:12px}
.wc-banner.show{display:flex}
.wc-banner .wc-b-icon{font-size:22px}
.wc-banner .wc-b-text{flex:1}
.wc-banner .wc-b-title{font-size:15px;font-weight:700;color:var(--gold);letter-spacing:.5px}
.wc-banner .wc-b-sub{font-size:11px;color:var(--t2);margin-top:1px}
.wc-banner .wc-b-info{text-align:right;font-size:11px;color:var(--t3);white-space:nowrap}
.wc-banner .wc-b-info .wc-b-num{font-size:20px;font-weight:800;color:var(--gold);font-family:var(--mono)}
.sd-wc-divider{height:1px;margin:8px 18px;background:linear-gradient(90deg,rgba(251,191,36,.12),transparent 60%)}

"""
c = c[:wc_css_idx] + wc_css + c[wc_css_idx:]
print("Added CSS")

# 3. Replace accToday + accPlan with accWC
# Use the actual HTML content to find boundaries
trophy = chr(0x1f3c6)
cal = chr(0x1f4c5)
chart = chr(0x1f4ca)
stadium = chr(0x1f3df)
money = chr(0x1f4b0)
star = chr(0x2b50)
arrow = chr(0x25b6)

sid_start = c.find('<div class="acc open" id="accToday"')
sid_end = c.find('<div class="acc" id="accHistory">')
if sid_start >= 0 and sid_end >= 0:
    new_sid = """    <div class="acc open" id="accWC">
      <div class="acc-head" onclick="toggleAccordion('accWC')">
        <span class="acc-arrow">""" + arrow + """</span>
        <span class="acc-icon">""" + trophy + """</span>
        <span class="acc-label">2026 """ + chr(0x4e16) + chr(0x754c) + chr(0x676f) + chr(0x5206) + chr(0x6790) + """</span>
        <span class="wc-badge">""" + chr(0x4e13) + chr(0x9898) + """</span>
        <span class="acc-count" id="wcMatchCount">-</span>
      </div>
      <div class="acc-body">
        <div class="acc-body-inner" style="padding:4px 0 8px">
          <div class="wc-sub-item active" data-view="today" onclick="switchWCView('today')">
            <span class="wsi-icon">""" + cal + """</span>
            <span class="wsi-label">""" + chr(0x4eca) + chr(0x65e5) + chr(0x8d5b) + chr(0x7a0b) + """</span>
          </div>
          <div class="wc-sub-item" data-view="standings" onclick="switchWCView('standings')">
            <span class="wsi-icon">""" + chart + """</span>
            <span class="wsi-label">""" + chr(0x5c0f) + chr(0x7ec4) + chr(0x79ef) + chr(0x5206) + chr(0x699c) + """</span>
          </div>
          <div class="wc-sub-item" data-view="bracket" onclick="switchWCView('bracket')">
            <span class="wsi-icon">""" + stadium + """</span>
            <span class="wsi-label">""" + chr(0x6dd8) + chr(0x6c70) + chr(0x8d5b) + chr(0x5bf9) + chr(0x9635) + chr(0x56fe) + """</span>
          </div>
          <div class="wc-sub-item" data-view="odds" onclick="switchWCView('odds')">
            <span class="wsi-icon">""" + money + """</span>
            <span class="wsi-label">""" + chr(0x51a0) + chr(0x519b) + chr(0x8d54) + chr(0x7387) + chr(0x8ffd) + chr(0x8e2a) + """</span>
          </div>
          <div class="wc-sub-item" data-view="picks" onclick="switchWCView('picks')">
            <span class="wsi-icon">""" + star + """</span>
            <span class="wsi-label">""" + chr(0x4eca) + chr(0x65e5) + chr(0x7cbe) + chr(0x9009) + chr(0x63a8) + chr(0x8350) + """</span>
          </div>
        </div>
      </div>
    </div>
    <div class="sd-wc-divider"></div>"""

    c = c[:sid_start] + new_sid + c[sid_end:]
    print("Replaced sidebar")
else:
    print("FAIL: sidebar boundaries not found!")

# 4. Add WC banner
banner = """  <div class="wc-banner show" id="wcBanner">
    <span class="wc-b-icon">""" + trophy + """</span>
    <div class="wc-b-text">
      <div class="wc-b-title">2026 """ + chr(0x4e16) + chr(0x754c) + chr(0x676f) + """ """ + chr(0xb7) + """ """ + chr(0x91cf) + chr(0x5316) + chr(0x5206) + chr(0x6790) + """</div>
      <div class="wc-b-sub" id="wcBannerSub">""" + chr(0x5c0f) + chr(0x7ec4) + chr(0x8d5b) + """ """ + chr(0xb7) + """ """ + chr(0x52a0) + chr(0x8f7d) + chr(0x4e2d) + """...</div>
    </div>
    <div class="wc-b-info">
      <div><span class="wc-b-num" id="wcRemainingCount">-</span></div>
      <div style="font-size:10px;color:var(--t3)">""" + chr(0x5269) + chr(0x4f59) + chr(0x573a) + chr(0x6b21) + """</div>
    </div>
  </div>
"""
c = c.replace('<div class="sec-header">', banner + '<div class="sec-header">')
print("Added banner")

# 5. Add switchWCView JS
wc_js = """function switchWCView(view){
  document.querySelectorAll(".wc-sub-item").forEach(function(x){x.classList.remove("active");});
  var el=document.querySelector('.wc-sub-item[data-view="'+view+'"]');
  if(el)el.classList.add("active");
  document.querySelectorAll(".wc-view").forEach(function(x){x.style.display="none";});
  var target=document.getElementById("wcView"+view.charAt(0).toUpperCase()+view.slice(1));
  if(target)target.style.display="block";
  var labels={today:""" + repr(chr(0x4eca)+chr(0x65e5)+chr(0x8d5b)+chr(0x7a0b)) + """,standings:""" + repr(chr(0x5c0f)+chr(0x7ec4)+chr(0x79ef)+chr(0x5206)+chr(0x699c)) + """,bracket:""" + repr(chr(0x6dd8)+chr(0x6c70)+chr(0x8d5b)+chr(0x5bf9)+chr(0x9635)+chr(0x56fe)) + """,odds:""" + repr(chr(0x51a0)+chr(0x519b)+chr(0x8d54)+chr(0x7387)+chr(0x8ffd)+chr(0x8e2a)) + """,picks:""" + repr(chr(0x4eca)+chr(0x65e5)+chr(0x7cbe)+chr(0x9009)+chr(0x63a8)+chr(0x8350)) + """};
  var h2=document.querySelector(".sec-header h2");
  if(h2)h2.textContent='""" + trophy + """ '+ (labels[view]||view);
}
"""
insert_js = "function toggleAccordion(id){var el=document.getElementById(id);if(el)el.classList.toggle('open');}"
c = c.replace(insert_js, wc_js + insert_js)
print("Added JS")

# 6. WC match count in loadToday
c = c.replace('todayMatchCount.textContent=tl+"', 'todayMatchCount.textContent=tl+"' + chr(0x573a) + '";try{document.getElementById("wcMatchCount").textContent=tl+"' + chr(0x573a) + '"}catch(e){}' + chr(0x0a) + '  document.getElementById("todayMatchCount").textContent=tl+"')
print("Updated match count")

# 7. Responsive CSS
c = c.replace(".plan-item,.acc .acc-label,.acc .acc-badge,.acc .acc-count,.hist-date-item .hd-date,.hist-date-item .hd-stats,.today-stat-row,.bt-item .bt-title,.bt-item .bt-meta,.doc-item .doc-title,.sd-contact,.sd-footer{display:none}", ".wc-sub-item,.plan-item,.acc .acc-label,.acc .acc-badge,.wc-badge,.acc .acc-count,.hist-date-item .hd-date,.hist-date-item .hd-stats,.today-stat-row,.bt-item .bt-title,.bt-item .bt-meta,.doc-item .doc-title,.sd-contact,.sd-footer{display:none}")
c = c.replace(".sd-wrap:hover .acc .acc-label,.sd-wrap:hover .acc .acc-badge,.sd-wrap:hover .acc .acc-count,.sd-wrap:hover .plan-item,.sd-wrap:hover .hist-date-item .hd-date,.sd-wrap:hover .hist-date-item .hd-stats,.sd-wrap:hover .today-stat-row,.sd-wrap:hover .bt-item .bt-title,.sd-wrap:hover .bt-item .bt-meta,.sd-wrap:hover .doc-item .doc-title,.sd-wrap:hover .sd-footer{display:flex;display:block}", ".sd-wrap:hover .wc-sub-item,.sd-wrap:hover .acc .acc-label,.sd-wrap:hover .acc .acc-badge,.sd-wrap:hover .wc-badge,.sd-wrap:hover .acc .acc-count,.sd-wrap:hover .plan-item,.sd-wrap:hover .hist-date-item .hd-date,.sd-wrap:hover .hist-date-item .hd-stats,.sd-wrap:hover .today-stat-row,.sd-wrap:hover .bt-item .bt-title,.sd-wrap:hover .bt-item .bt-meta,.sd-wrap:hover .doc-item .doc-title,.sd-wrap:hover .sd-footer{display:flex;display:block}")
print("Updated responsive CSS")

# 8. Title
title_find = "<title>V3.3.3-Core " + chr(0x5206) + chr(0x6790) + chr(0x7cfb) + chr(0x7edf) + "</title>"
title_repl = "<title>V3.3.3-Core 2026 " + chr(0x4e16) + chr(0x754c) + chr(0x676f) + chr(0x5206) + chr(0x6790) + "</title>"
c = c.replace(title_find, title_repl)
print("Updated title")

# Write
with open("D:/V3.3.3-Core/templates/index.html", "w", encoding="utf-8") as f:
    f.write(c)
print("DONE - written", len(c), "bytes")
