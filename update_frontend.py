with open("D:/V3.3.3-Core/templates/index.html","r",encoding="utf-8-sig") as f:
    c = f.read()

idx = c.find("function switchWCView")
end = c.find("function toggleAccordion", idx)

new_js = """function switchWCView(view){
  document.querySelectorAll(".wc-sub-item").forEach(function(x){x.classList.remove("active");});
  var el=document.querySelector('.wc-sub-item[data-view="'+view+'"]');
  if(el)el.classList.add("active");
  document.querySelectorAll(".wc-view").forEach(function(x){x.style.display="none";});
  var target=document.getElementById("wcView"+view.charAt(0).toUpperCase()+view.slice(1));
  if(target)target.style.display="block";
  var labels={today:"\u4eca\u65e5\u8d5b\u7a0b",standings:"\u5c0f\u7ec4\u79ef\u5206\u699c",bracket:"\u6dd8\u6c70\u8d5b\u5bf9\u9635\u56fe",odds:"\u51a0\u519b\u8d54\u7387\u8ffd\u8e2a",picks:"\u4eca\u65e5\u7cbe\u9009\u63a8\u8350"};
  var h2=document.querySelector(".sec-header h2");
  if(h2)h2.textContent="\\U0001f3c6 "+ (labels[view]||view);
  if(view=="today")loadWCSchedule();
}

function loadWCSchedule(){
  var el=document.getElementById("loadWCSchedule");
  if(el)el.click();
  var container=document.getElementById("wcViewToday");
  if(!container)return;
  if(container.getAttribute("data-loaded")=="1")return;
  container.setAttribute("data-loaded","1");
  container.innerHTML="<div class=sd-loading>\u52a0\u8f7d\u8d5b\u7a0b\u4e2d...</div>";
  fetch("/api/wc/schedule").then(function(r){return r.json()}).then(function(d){
    if(!d||!d.matches||d.matches.length===0){
      container.innerHTML="<div class=empty-state>\u6682\u65e0\u8d5b\u7a0b\u6570\u636e</div>";
      return;
    }
    var html="";
    var byDate={};
    d.matches.forEach(function(m){
      var dt=m.date||"";
      if(!byDate[dt])byDate[dt]=[];
      byDate[dt].push(m);
    });
    Object.keys(byDate).forEach(function(dt){
      var ms=byDate[dt];
      html+='<div class="sec-header" style="margin-top:0;padding:14px 0 6px"><h2 style="font-size:13px;color:var(--gold);font-weight:700;letter-spacing:.5px">'+dt+'</h2><div class="sec-bar"></div></div>';
      ms.forEach(function(m){
        var gb='<span style="font-size:10px;color:var(--gold);background:rgba(251,191,36,.1);padding:1px 6px;border-radius:3px;border:1px solid rgba(251,191,36,.15);font-weight:600">'+m.group+'</span>';
        var timeStr=m.time||"--:--";
        var oh="";
        if(m.odds){
          var o=m.odds;
          oh='<div style="display:flex;gap:4px;font-size:10px;font-family:var(--mono);color:var(--t3)"><span>\u80dc <b style=color:var(--t1);font-weight:600>'+o.sp_h+'</b></span><span>\u5e73 <b style=color:var(--t1);font-weight:600>'+o.sp_d+'</b></span><span>\u8d1f <b style=color:var(--t1);font-weight:600>'+o.sp_a+'</b></span></div>';
        }
        html+='<div class="wc-card" style="background:rgba(16,22,42,.78);border:1px solid rgba(255,255,255,.06);border-radius:8px;padding:10px 14px;margin-bottom:6px">';
        html+='<div style="display:flex;align-items:center;gap:8px;justify-content:space-between;flex-wrap:wrap">';
        html+='<div style="display:flex;align-items:center;gap:6px"><span style="font-size:11px;color:var(--t3);font-family:var(--mono);min-width:36px">'+timeStr+'</span>'+gb+'</div>';
        html+=oh;
        html+='</div>';
        html+='<div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-top:6px">';
        html+='<div style="display:flex;align-items:center;gap:4px;flex:1;justify-content:flex-end"><span style="font-size:16px">'+(m.home_flag||"")+'</span><span style="font-size:14px;font-weight:700;color:var(--t1)">'+m.home+'</span></div>';
        html+='<span style="font-size:11px;color:var(--t3);font-weight:600">VS</span>';
        html+='<div style="display:flex;align-items:center;gap:4px;flex:1;justify-content:flex-start"><span style="font-size:14px;font-weight:700;color:var(--t1)">'+m.away+'</span><span style="font-size:16px">'+(m.away_flag||"")+'</span></div>';
        html+='</div></div>';
      });
    });
    container.innerHTML=html;
  }).catch(function(){
    container.innerHTML="<div class=empty-state>\u52a0\u8f7d\u5931\u8d25</div>";
  });
}
"""

c = c[:idx] + new_js + c[end:]
with open("D:/V3.3.3-Core/templates/index.html","w",encoding="utf-8") as f:
    f.write(c)
print("Updated! Written", len(c), "bytes")
