var _DATA=null,RV=[],SORT_BY="id",FILTER={rating:{'S':true,'A':true,'B':true,'C':true},event:{}};FILTER_ALL_EVENTS=true;FILTER_SHOW=false;
function loadReviews(){
  fetch('/api/reviews').then(function(r){return r.json();}).then(function(d){if(d&&d.length){RV=d;renderReview();}}).catch(function(){});
}

function badge(r,f){
  var g=gr(r,f);
  return'<span class="badge badge-'+g.toLowerCase()+'">'+g+'</span>';
}
function rtClass(r,f){
  var g=gr(r,f);
  return'rt-'+g.toLowerCase();
}
function dirTag(d){
  if(d.indexOf('\u4e3b')>=0)return'<span class="dir dir-h"><i></i>\u4e3b\u80dc</span>';
  if(d.indexOf('\u5ba2')>=0)return'<span class="dir dir-a"><i></i>\u5ba2\u80dc</span>';
  if(d.indexOf('\u5e73')>=0)return'<span class="dir dir-d"><i></i>\u5e73\u5c40</span>';
  return'<span class="dir">'+d+'</span>';
}
function gr(ra,fs){
  if(ra==='S'||fs>=9)return'S';
  if(ra==='A'||fs>=7)return'A';
  if(ra==='C')return'C';
  if(fs>=5)return'B';
  return'C';
}
function toggleFilter(){
  FILTER_SHOW=!FILTER_SHOW;
  var d=document.getElementById("filterDropdown");
  if(d){d.style.display=FILTER_SHOW?"block":"none";}
}
function setFilter(type,val){
  if(type==="rating"){
    FILTER.rating[val]=!FILTER.rating[val];
    var allTrue=true;
    for(var k in FILTER.rating){if(!FILTER.rating[k]){allTrue=false;break;}}
    if(allTrue){FILTER.rating={'S':true,'A':true,'B':true,'C':true};}
  }else if(type==="event"){
    FILTER.event[val]=!FILTER.event[val];
    FILTER_ALL_EVENTS=false;
    var allEv=true;
    for(var k in FILTER.event){if(!FILTER.event[k]){allEv=false;break;}}
    if(allEv){FILTER_ALL_EVENTS=true;FILTER.event={};}
  }else if(type==="event_all"){
    FILTER_ALL_EVENTS=!FILTER_ALL_EVENTS;
    if(FILTER_ALL_EVENTS){FILTER.event={};}
  }
  if(_DATA)rs(_DATA);
}
function filterLabel(){
  var rk=['S','A','B','C'],sel=rk.filter(function(l){return FILTER.rating[l];});
  return sel.length===4?'全部等级':sel.join('/')+'级';
}
function buildSummary(d){
  var r=d.rating||[],ts=0,c={S:0,A:0,B:0,C:0};
  r.forEach(function(x){ts+=x.fit_score||0;
    var g=gr(x.rating,x.fit_score);c[g]++;});
  var avg=r.length?(ts/r.length).toFixed(1):'0',t=r.length||1;
  var h='<div><b>'+t+'</b> \u573a</div><div><b>'+avg+'</b> \u5e73\u5747</div>';
  if(c.S)h+='<div>S<b>'+c.S+'</b></div>';if(c.A)h+='<div>A<b>'+c.A+'</b></div>';
  if(c.B)h+='<div>B<b>'+c.B+'</b></div>';if(c.C)h+='<div>C<b>'+c.C+'</b></div>';
  document.getElementById('stats').innerHTML=h;
  var rd='',cols={S:'#1B365D',A:'#b8943a',B:'#4a7a5a',C:'#6b6a64'};
  if(c.S)rd+='<div style="width:'+(c.S/t*100).toFixed(1)+'%;background:'+cols.S+'"></div>';
  if(c.A)rd+='<div style="width:'+(c.A/t*100).toFixed(1)+'%;background:'+cols.A+'"></div>';
  if(c.B)rd+='<div style="width:'+(c.B/t*100).toFixed(1)+'%;background:'+cols.B+'"></div>';
  if(c.C)rd+='<div style="width:'+(c.C/t*100).toFixed(1)+'%;background:'+cols.C+'"></div>';
  document.getElementById('rd').innerHTML=rd;
}
function buildCharts(card,mid){
  if(card.querySelector('.cb'))return;
  var NS='http://www.w3.org/2000/svg';
  var ratings=_DATA.rating||[],mcs=_DATA.mc||[],ddis=_DATA.ddi||[];
  var idx=-1;
  for(var i=0;i<ratings.length;i++){if(ratings[i].id===mid){idx=i;break;}}
  if(idx<0)return;
  var mc=mcs[idx]||{},dd=ddis[idx]||{};
  var mp=mc.physical||{},mk=dd.p_market||{};
  var phw=mp.home_win||0,pdw=mp.draw||0,paw=mp.away_win||0;
  var mhw=mk.home_win||0,mdw=mk.draw||0,maw=mk.away_win||0;
  var dH=(dd.ddi||{}).home_win||0;
  var lh=mc.lambda_h_final||0,la=mc.lambda_a_final||0,ld=mc.lambda_diff||(lh-la);
  var row=card.querySelector('.charts-row');
  if(!row)return;
  var c1=document.createElement('div');c1.className='cb';
  c1.innerHTML='<div class="ct">\u03bb \u5bf9\u6bd4</div>';
  var s1=document.createElementNS(NS,'svg');
  s1.setAttribute('width','100%');s1.setAttribute('height','140');s1.setAttribute('viewBox','0 0 260 140');
  var maxV=Math.max(lh,la,1.5)*1.25,bW=55,gap=40,cH=90,cY=30,bX1=(260-bW*2-gap)/2;
  for(var gi=0;gi<=4;gi++){
    var v=(maxV/4)*gi,y=cY+cH-(v/maxV)*cH;
    var gl=document.createElementNS(NS,'line');
    gl.setAttribute('x1','32');gl.setAttribute('y1',y);gl.setAttribute('x2','250');gl.setAttribute('y2',y);
    gl.setAttribute('stroke','var(--bd)');gl.setAttribute('stroke-width','1');s1.appendChild(gl);
    var gt=document.createElementNS(NS,'text');
    gt.setAttribute('x','28');gt.setAttribute('y',y+3);gt.setAttribute('fill','var(--t3)');
    gt.setAttribute('font-size','12');gt.setAttribute('text-anchor','end');
    gt.setAttribute('font-family','SF Mono,Consolas,monospace');
    gt.textContent=v.toFixed(1);s1.appendChild(gt);
  }
  function mb(x,y,w,h,c,v,l){
    var r=document.createElementNS(NS,'rect');
    r.setAttribute('x',x);r.setAttribute('y',y);r.setAttribute('width',w);r.setAttribute('height',h);
    r.setAttribute('rx','4');r.setAttribute('fill',c);r.setAttribute('opacity','0.85');s1.appendChild(r);
    var t=document.createElementNS(NS,'text');
    t.setAttribute('x',x+w/2);t.setAttribute('y',y-5);t.setAttribute('fill','var(--t1)');
    t.setAttribute('font-size','12');t.setAttribute('font-weight','600');t.setAttribute('text-anchor','middle');
    t.setAttribute('font-family','SF Mono,Consolas,monospace');t.textContent=v;s1.appendChild(t);
    var lb=document.createElementNS(NS,'text');
    lb.setAttribute('x',x+w/2);lb.setAttribute('y',cY+cH+11);lb.setAttribute('fill','var(--t3)');
    lb.setAttribute('font-size','11');lb.setAttribute('text-anchor','middle');lb.textContent=l;s1.appendChild(lb);
  }
  mb(bX1,cY+cH-Math.max((lh/maxV)*cH,3),bW,Math.max((lh/maxV)*cH,3),'var(--ink)',lh.toFixed(3),'\u03bb\u4e3b');
  mb(bX1+bW+gap,cY+cH-Math.max((la/maxV)*cH,3),bW,Math.max((la/maxV)*cH,3),'var(--red)',la.toFixed(3),'\u03bb\u5ba2');
  var tt=document.createElementNS(NS,'text');
  tt.setAttribute('x','32');tt.setAttribute('y','13');tt.setAttribute('fill','var(--amber)');
  tt.setAttribute('font-size','12');tt.setAttribute('font-weight','600');
  tt.setAttribute('font-family','SF Mono,Consolas,monospace');tt.textContent='\u0394 '+ld.toFixed(3);s1.appendChild(tt);
  var dc=Math.abs(dH)>0.05?'var(--red)':'var(--green)';
  var dt=document.createElementNS(NS,'text');
  dt.setAttribute('x','248');dt.setAttribute('y','13');dt.setAttribute('fill',dc);
  dt.setAttribute('font-size','11');dt.setAttribute('font-weight','500');dt.setAttribute('text-anchor','end');
  dt.setAttribute('font-family','SF Mono,Consolas,monospace');
  dt.textContent='DDI '+(dH>=0?'+':'')+dH.toFixed(4);s1.appendChild(dt);
  c1.appendChild(s1);row.appendChild(c1);
  var c2=document.createElement('div');c2.className='cb';
  c2.innerHTML='<div class="ct">\u7269\u7406 vs \u5e02\u573a</div>';
  var s2=document.createElementNS(NS,'svg');
  s2.setAttribute('width','100%');s2.setAttribute('height','140');s2.setAttribute('viewBox','0 0 260 140');
  var barW=34,barG=5,cH2=90,cY2=30;
  var groups=[['\u4e3b\u80dc',phw,mhw,dH],['\u5e73\u5c40',pdw,mdw,0],['\u5ba2\u80dc',paw,maw,-dH]];
  var maxP=1;groups.forEach(function(g){maxP=Math.max(maxP,g[1],g[2]);});
  maxP=Math.ceil(maxP*100/5)*5+5;maxP=Math.max(maxP,55)/100;
  for(var pi=0;pi<=maxP*100;pi+=10){
    var y2=cY2+cH2-(pi/100/maxP)*cH2;
    var ln=document.createElementNS(NS,'line');
    ln.setAttribute('x1','32');ln.setAttribute('y1',y2);ln.setAttribute('x2','250');ln.setAttribute('y2',y2);
    ln.setAttribute('stroke','var(--bd)');ln.setAttribute('stroke-width','1');s2.appendChild(ln);
    var tx=document.createElementNS(NS,'text');
    tx.setAttribute('x','28');tx.setAttribute('y',y2+3);tx.setAttribute('fill','var(--t3)');
    tx.setAttribute('font-size','10');tx.setAttribute('text-anchor','end');
    tx.setAttribute('font-family','SF Mono,Consolas,monospace');tx.textContent=pi+'%';s2.appendChild(tx);
  }
  var gap2=6,tw=groups.length*(barW*2+barG)+gap2*2;
  var sx=32+(260-32-tw)/2;
  groups.forEach(function(g,i){
    var x=sx+i*((barW*2+barG)+gap2);
    var b1=Math.max((g[1]/maxP)*cH2,3);
    var rp=document.createElementNS(NS,'rect');
    rp.setAttribute('x',x);rp.setAttribute('y',cY2+cH2-b1);rp.setAttribute('width',barW);rp.setAttribute('height',b1);
    rp.setAttribute('rx','2');rp.setAttribute('fill','var(--ink)');rp.setAttribute('opacity','0.85');s2.appendChild(rp);
    var tv1=document.createElementNS(NS,'text');
    tv1.setAttribute('x',x+barW/2);tv1.setAttribute('y',cY2+cH2-b1-4);
    tv1.setAttribute('fill','var(--ink)');tv1.setAttribute('font-size','11');tv1.setAttribute('font-weight','600');
    tv1.setAttribute('text-anchor','middle');tv1.setAttribute('font-family','SF Mono,Consolas,monospace');
    tv1.textContent=(g[1]*100).toFixed(1)+'%';s2.appendChild(tv1);
    var x2=x+barW+barG,b2=Math.max((g[2]/maxP)*cH2,3);
    var rm=document.createElementNS(NS,'rect');
    rm.setAttribute('x',x2);rm.setAttribute('y',cY2+cH2-b2);rm.setAttribute('width',barW);rm.setAttribute('height',b2);
    rm.setAttribute('rx','2');rm.setAttribute('fill','var(--red)');rm.setAttribute('opacity','0.8');s2.appendChild(rm);
    var tv2=document.createElementNS(NS,'text');
    tv2.setAttribute('x',x2+barW/2);tv2.setAttribute('y',cY2+cH2-b2-4);
    tv2.setAttribute('fill','var(--red)');tv2.setAttribute('font-size','11');tv2.setAttribute('font-weight','600');
    tv2.setAttribute('text-anchor','middle');tv2.setAttribute('font-family','SF Mono,Consolas,monospace');
    tv2.textContent=(g[2]*100).toFixed(1)+'%';s2.appendChild(tv2);
    var lbl=document.createElementNS(NS,'text');
    lbl.setAttribute('x',x+barW+barG/2);lbl.setAttribute('y',cY2+cH2+11);
    lbl.setAttribute('fill','var(--t3)');lbl.setAttribute('font-size','11');lbl.setAttribute('text-anchor','middle');
    lbl.textContent=g[0];s2.appendChild(lbl);
    var dv=g[3],dc2=Math.abs(dv)>0.05?'var(--red)':'var(--green)';
    var dt2=document.createElementNS(NS,'text');
    dt2.setAttribute('x',x+barW+barG/2);dt2.setAttribute('y',cY2+cH2+21);
    dt2.setAttribute('fill',dc2);dt2.setAttribute('font-size','9');dt2.setAttribute('text-anchor','middle');
    dt2.setAttribute('font-family','SF Mono,Consolas,monospace');
    dt2.textContent=(dv>=0?'+':'')+dv.toFixed(3);s2.appendChild(dt2);
    if(i===0&&Math.abs(g[1]-g[2])>0.02){
      var mx=x+barW+barG/2,ay=cY2+cH2-Math.max(b1,b2)-9;
      var ar=document.createElementNS(NS,'text');
      ar.setAttribute('x',mx);ar.setAttribute('y',ay);
      ar.setAttribute('fill','var(--amber)');ar.setAttribute('font-size','10');ar.setAttribute('font-weight','700');ar.setAttribute('text-anchor','middle');
      ar.setAttribute('font-family','SF Mono,Consolas,monospace');
      ar.textContent='\u0394'+((g[1]-g[2])*100).toFixed(1)+'%';s2.appendChild(ar);
    }
  });
  var lg1=document.createElementNS(NS,'text');
  lg1.setAttribute('x','150');lg1.setAttribute('y','13');
  lg1.setAttribute('fill','var(--ink)');lg1.setAttribute('font-size','10');lg1.setAttribute('font-weight','500');
  lg1.setAttribute('font-family','SF Mono,Consolas,monospace');lg1.textContent='\u25a0 \u7269\u7406';s2.appendChild(lg1);
  var lg2=document.createElementNS(NS,'text');
  lg2.setAttribute('x','200');lg2.setAttribute('y','13');
  lg2.setAttribute('fill','var(--red)');lg2.setAttribute('font-size','10');lg2.setAttribute('font-weight','500');
  lg2.setAttribute('font-family','SF Mono,Consolas,monospace');lg2.textContent='\u25a0 \u5e02\u573a';s2.appendChild(lg2);
  c2.appendChild(s2);row.appendChild(c2);
}
function rs(d){
  _DATA=d;
  loadReviews();
  _DATA=d;buildSummary(d);
  var r=d.rating,mi=d.info||[],dd=d.ddi||[],ai=d.ai||[],mc=d.mc||[];
  var im={},dm={},am={},mm={};
  mi.forEach(function(m){im[m.id]=m;});dd.forEach(function(m){dm[m.id]=m;});
  ai.forEach(function(m){am[m.id]=m;});mc.forEach(function(m){mm[m.id]=m;});
  var s=[].concat(r).filter(function(x){var g=gr(x.rating,x.fit_score);var ev=x.event||'';var evOk=FILTER_ALL_EVENTS||!ev||FILTER.event[ev];return FILTER.rating[g]&&evOk;}).sort(function(a,b){return SORT_BY==="fit"?b.fit_score-a.fit_score:a.id.localeCompare(b.id);});
  var h='<div class="sec"><span class="sec-dot"></span><span class="sec-h">今日扫盘</span>' +'<select id="sortSelect" style="margin-left:12px;background:var(--surface-2);border:1px solid var(--bd);border-radius:4px;padding:2px 6px;font-size:11px;color:var(--t2);font-family:var(--sans);outline:none;cursor:pointer" onchange="SORT_BY=this.value;if(_DATA)rs(_DATA);">' +'<option value="id"'+(SORT_BY==='id'?' selected':'')+'>编号</option>' +'<option value="fit"'+(SORT_BY==='fit'?' selected':'')+'>推荐度</option>' +'</select>' +'<div style="position:relative;margin-left:8px;display:inline-block">' +'<span onclick="toggleFilter()" style="cursor:pointer;background:var(--surface-2);border:1px solid var(--bd);border-radius:4px;padding:2px 8px;font-size:11px;color:var(--t2);font-family:var(--sans);white-space:nowrap;user-select:none">筛选 ▼</span>' +'<div id="filterDropdown" style="display:none;position:absolute;top:100%;left:0;margin-top:4px;background:var(--surface);border:1px solid var(--bd);border-radius:6px;padding:8px;z-index:50;min-width:130px;box-shadow:0 4px 16px rgba(0,0,0,0.1)">' +'<div style="font-size:10px;color:var(--t3);font-weight:600;margin-bottom:4px;letter-spacing:0.3px">推荐等级</div>' +['S','A','B','C'].map(function(l){return'<label style="display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px"><input type="checkbox" '+(FILTER.rating[l]?'checked':'')+' onchange="setFilter(\'rating\',\''+l+'\')" style="margin:0"><span>'+l+'级</span></label>';})+'<div style="border-top:1px solid var(--bd);margin:6px 0 4px;padding-top:6px">'+'<div style="font-size:10px;color:var(--t3);font-weight:600;margin-bottom:4px;letter-spacing:0.3px">赛事类型</div>'+'<label style="display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px"><input type="checkbox" '+(FILTER_ALL_EVENTS?'checked':'')+' onchange="setFilter(\'event_all\',\'all\')" style="margin:0"><span>全部赛事</span></label>'+_DATA.rating.reduce(function(acc,x){var ev=x.event||'';if(ev&&acc.indexOf(ev)<0)acc.push(ev);return acc;},[]).map(function(ev){return'<label style="display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px"><input type="checkbox" '+(FILTER_ALL_EVENTS||FILTER.event[ev]?'checked':'')+' onchange="setFilter(\'event\',\''+ev+'\')" style="margin:0"><span>'+ev+'</span></label>';}).join('')+'</div>'+'</div></div>' +'<span class="sec-l"></span></div>';
h+='<div class="thr"><span>赛事编号</span><span>开始时间</span><span>主队vs客队</span><span>胜平负</span><span>总进球</span><span>半全场</span><span>比分</span><span>推荐度</span></div>';
  s.forEach(function(x){
    var m=im[x.id]||{},mc2=mm[x.id]||{},dr=dm[x.id]||{},ar=am[x.id]||{};
    var p=mc2.physical||{};
    var hw=(p.home_win||0)*100,dw=(p.draw||0)*100,aw=(p.away_win||0)*100;
    var dh=(dr.ddi||{}).home_win||0,s7=ar.s7_score||0;
    var lh=mc2.lambda_h_final||0,la=mc2.lambda_a_final||0;
    var ah=m.asian_handicap||0,hs=ah===0?'0':(ah>0?'+'+ah.toFixed(1):ah.toFixed(1));
    var tm=m.time||'',ko=tm.length>=16?tm.substring(5,10)+' '+tm.substring(11,16):'';
    var mid=x.id,dCls=Math.abs(dh)>0.05?'hot':'ok',sCls=s7>0?'warn':'',st=m.event||m.scenario_type||'';
    var g2=mc2.top2_total_goals||[],h2=mc2.top2_half_full||[],s3=mc2.top3_scores||[];
    var gs=g2.join('/'),hs2=h2.join('/'),ss=s3.join('/');
    var trap=ar.trap_analysis||'',risk=ar.key_risk||'',s7r=ar.s7_reason||'',ld=mc2.lambda_diff||0;
    h+='<div class="card '+rtClass(x.rating,x.fit_score)+'" data-mid="'+mid+'"><div class="cg2">';
    h+='<div class="c2-col c2-id"><span class="c-id">#'+mid+'</span></div>';
    h+='<div class="c2-col c2-tm"><span class="c-ti">'+ko+'</span></div>';
    h+='<div class="c2-col c2-mm"><span class="c2-h">'+x.home+'</span><span class="c2-v">vs</span><span class="c2-a">'+x.away+'</span><span class="tag2">'+st+'</span></div>';
    h+='<div class="c2-col c2-dr">'+dirTag(x.direction)+'</div>';
    h+='<div class="c2-col c2-g">'+gs+'</div>';
    h+='<div class="c2-col c2-ht">'+hs2+'</div>';
    h+='<div class="c2-col c2-scr">'+ss+'</div>';
    h+='<div class="c2-col c2-r"><div class="c-sc2">'+x.fit_score.toFixed(1)+'</div>'+badge(x.rating,x.fit_score)+'</div>';
    h+='</div><div class="cg2b">';
    h+='<div class="prob2"><div class="prob-b"><div style="width:'+hw.toFixed(1)+'%;background:var(--green)"></div><div style="width:'+dw.toFixed(1)+'%;background:var(--amber)"></div><div style="width:'+aw.toFixed(1)+'%;background:var(--red)"></div></div><span class="prob-n">'+Math.round(hw)+'/'+Math.round(dw)+'/'+Math.round(aw)+'</span></div>';
    h+='<div class="c2-s"><span class="cs-l cs-l-lg">λ</span><span class="cs-v">'+lh.toFixed(2)+'/'+la.toFixed(2)+'</span><span class="c2-sp">|</span><span class="cs-l">DDI</span><span class="cs-v '+dCls+'">'+(dh>=0?'+':'')+dh.toFixed(3)+'</span><span class="c2-sp">|</span><span class="cs-l">S7</span><span class="cs-v '+sCls+'">'+s7+'</span><span class="c2-sp">|</span><span class="cs-l">盘口</span><span class="cs-v">'+hs+'</span></div>';
    h+='</div>';
    h+='<div class="cd"><div class="charts-row"></div><div class="ana">';
    h+='<div class="ana-i"><span class="ana-l">λ差值</span><span>'+ld.toFixed(3)+'</span></div>';
    if(s7r)h+='<div class="ana-i"><span class="ana-l">S7 说明</span><span>'+s7r+'</span></div>';
    if(trap)h+='<div class="ana-i"><span class="ana-l">诱盘分析</span><span>'+trap+'</span></div>';
    if(risk)h+='<div class="ana-i risk"><span class="ana-l">风险提示</span><span>'+risk+'</span></div>';
    h+='</div></div></div>';
  });
  document.getElementById('r').innerHTML=h;
  document.querySelectorAll('.card').forEach(function(c){
    c.addEventListener('click',function(){
      var e=this.classList.contains('expanded');
      document.querySelectorAll('.card.expanded').forEach(function(x){x.classList.remove('expanded');});
      if(!e){this.classList.add('expanded');buildCharts(this,this.getAttribute('data-mid'));}
    });
  });
}



function renderReview(){
  var yr=RV.filter(function(m){return m.date&&m.actual_score&&m.actual_score!=='--';});
  var yd=yr.length?new Date(yr[0].date):new Date();
  if(yr.length){var ym={};yr.forEach(function(m){var d=m.date.substring(0,10);ym[d]=(ym[d]||0)+1;});
  var ds=Object.keys(ym).sort().reverse();var ys=ds[0];
  yr=RV.filter(function(m){return m.date&&m.date.indexOf(ys)===0;});
  var dp=ys.split('-');yd=new Date(parseInt(dp[0]),parseInt(dp[1])-1,parseInt(dp[2]));}
  var h='<div class="sec"><span class="sec-dot"></span><span class="sec-h">昨日扫盘</span><span class="sec-l"></span></div>';
  // 复盘统计
  if(yr.length&&_DATA&&_DATA.rating){
    var rCnt=yr.length,rHits=yr.filter(function(x){return x.hit==='True';}).length,rRate=Math.round(rHits/rCnt*100);
    var rSt={S:{t:0,h:0},A:{t:0,h:0},B:{t:0,h:0},C:{t:0,h:0}};
    yr.forEach(function(mx){
      var fs=mx.fit_score||0;
      var ra=mx.rating||'';
      var rt=gr(ra,fs);
      if(rSt[rt]){rSt[rt].t++;if(mx.hit==='True')rSt[rt].h++;}
    });
    var ds=new Date(yd.getTime()-86400000).getFullYear()+'.'+(new Date(yd.getTime()-86400000).getMonth()+1)+'.'+new Date(yd.getTime()-86400000).getDate();
    var hb='<span style="font-size:13px;font-weight:400;color:var(--t2);margin-left:8px;white-space:nowrap">';
    hb+=ds+'&emsp;&emsp;扫盘 '+rCnt+' 场&emsp;&emsp;命中'+rHits+'场&emsp;&emsp;命中率'+rRate+'%&emsp;&emsp;&emsp;';
    var rK=['S','A','B','C'],rC={S:'#1B365D',A:'#b8943a',B:'#4a7a5a',C:'#6b6a64'};
    for(var ri=0;ri<rK.length;ri++){var rk=rK[ri];if(rSt[rk].t>0){
      hb+='&emsp;<span style="color:'+rC[rk]+';font-weight:600">'+rk+'级'+rSt[rk].t+'中'+rSt[rk].h+'</span>';
    }}
    hb+='</span>';
    h=h.replace('<span class="sec-l">', hb+'<span class="sec-l">');
  }
  if(yr.length){
    h+='<div class="thr"><span class="c2-id">赛事编号</span><span class="c2-tm">开始时间</span><span class="c2-mm">主队vs客队</span><span class="c2-dr">胜平负</span><span style="width:210px;text-align:center">赛果</span><span style="width:90px;text-align:center;padding-left:40px">命中</span><span style="width:110px;text-align:right;padding-right:28px">推荐度</span></div>';
    yr.forEach(function(m){
      var hit=m.hit==='True';
      var rt=hit?'rt-hit':'rt-miss';
      var d=m.date||'';var ko=d.length>=16?d.substring(5,10)+' '+d.substring(11,16):'';
      var dir=m.direction||'';
      var score=m.actual_score||'--';
      var diag=m.diagnosis||'';
      var dTag=dirTag(dir);
      var tg='\u2014';
      if(score.indexOf('-')>=0){var sp=score.split('-');var t=parseInt(sp[0])+parseInt(sp[1]);if(!isNaN(t))tg=t+'\u7403';}
      var htftData={'003':'平胜','004':'负负','005':'负胜','006':'负平','007':'胜胜','008':'平胜','009':'胜胜'};
      var ht=htftData[m.id]||'\u2014';
      var scCol=hit?'#c0392b':'var(--t1)';
      h+='<div class="card '+rt+'"><div class="cg2">';
      h+=['<div class="c2-col c2-id"><span class="c-id">#'+m.id+'</span></div>',
          '<div class="c2-col c2-tm"><span class="c-ti">'+ko+'</span></div>',
          '<div class="c2-col c2-mm"><span class="c2-h">'+m.home+'</span><span class="c2-v">vs</span><span class="c2-a">'+m.away+'</span></div>',
          '<div class="c2-col c2-dr" style="color:'+scCol+'">'+dTag+'</div>',
          '<div class="c2-col" style="width:210px;text-align:center;font-family:var(--mono);font-size:14px;font-weight:600;color:'+scCol+'">'+score+'/'+ht+'</div>',
          '<div class="c2-col" style="width:90px;text-align:center;padding-left:40px"><span style="display:inline-block;background:'+(hit?'#c0392b':'#555')+';color:#fff;font-size:11px;padding:2px 10px;border-radius:3px;font-weight:600;letter-spacing:0.5px">'+(hit?'命中':'未中')+'</span></div>',
        '<div class="c2-col" style="width:110px;text-align:right;padding-right:14px;font-family:var(--mono);font-size:13px;font-weight:600;color:var(--ink)">' + (m.fit_score ? m.fit_score.toFixed(1) : '--') + ' ' + (m.rating ? '<span class="badge badge-' + m.rating.toLowerCase() + '">' + m.rating + '</span>' : '') + '</div>'
      ].join('');
      h+='</div>';
      // Expanded — prediction details (combined row)
      var predDir=m.direction||'\u2014';
      var predGoals='\u2014';
      var predHT='\u2014';
      var predScore='\u2014';
      var fitScore=m.fit_score||0;
      var rtRating=m.rating||'';
      var lambdaD=m.lambda_diff||0;
      var scType=m.scenario_type||'';
      var ddiVal=m.ddi_home_win||0;
      if(m.top2_total_goals&&typeof m.top2_total_goals==='string'){
        try{predGoals=JSON.parse(m.top2_total_goals).join('/');}catch(e){predGoals=m.top2_total_goals;}
      }else if(m.top2_total_goals instanceof Array){predGoals=m.top2_total_goals.join('/');}
      if(m.top2_half_full&&typeof m.top2_half_full==='string'){
        try{predHT=JSON.parse(m.top2_half_full).join('/');}catch(e){predHT=m.top2_half_full;}
      }else if(m.top2_half_full instanceof Array){predHT=m.top2_half_full.join('/');}
      if(m.top3_scores&&typeof m.top3_scores==='string'){
        try{predScore=JSON.parse(m.top3_scores).join('/');}catch(e){predScore=m.top3_scores;}
      }else if(m.top3_scores instanceof Array){predScore=m.top3_scores.join('/');}
      // Highlight individual correct items
      function hl(v,c){return c?'<span style="color:#c0392b;font-weight:600">'+v+'</span>':v;}
      var dirHtml=hl(predDir,hit);
      var goalsHtml=predGoals;
      if(tg!=='\u2014'&&predGoals!=='\u2014'){
        var gn=parseInt(tg);
        if(!isNaN(gn)){goalsHtml=predGoals.split('/').map(function(g){return hl(g,parseInt(g)===gn);}).join('/');}
      }
      var htHtml=predHT;
      if(ht!=='\u2014'&&predHT!=='\u2014'){htHtml=predHT.split('/').map(function(h){return hl(h,h===ht);}).join('/');}
      var scHtml=predScore;
      if(predScore!=='\u2014'){scHtml=predScore.split('/').map(function(s){return hl(s,s===score);}).join('/');}
      if(predGoals==='—'&&predHT==='—'&&predScore==='—'){
        var dh='<div class="ana-i" style="grid-column:1/-1"><span class="ana-l">预测</span><span style="font-family:var(--mono);font-size:13px;line-height:1.8">'+
          dirHtml+'</span></div>';
      }else{
        var dh='<div class="ana-i" style="grid-column:1/-1"><span class="ana-l">预测明细</span><span style="font-family:var(--mono);font-size:13px;line-height:1.8">'+
          dirHtml+' ｜ '+goalsHtml+' ｜ '+htHtml+' ｜ '+scHtml+'</span></div>';
      }
      // Detailed conclusion
      var cl='';
      if(hit){
        cl='\u6846\u67b6\u652f\u6491\u5206\u6790\uff1a';
        if(fitScore>=7)cl+='\u7efc\u5408\u9002\u914d\u5ea6'+fitScore.toFixed(1)+'\u5206\uff08\u8f83\u9ad8\uff09\uff0c\u8bc4\u7ea7'+rtRating+'，';
        if(Math.abs(lambdaD)>0.5)cl+='\u03bb\u5dee\u5f02\u5ea6'+lambdaD.toFixed(3)+'\uff08\u6a21\u578b\u533a\u5206\u660e\u663e\uff09\uff0c';
        cl+='DDI\u6821\u51c6'+(Math.abs(ddiVal)>0.05?'\u660e\u663e\uff08'+ddiVal.toFixed(3)+'\uff09\uff0c\u5e02\u573a\u70ed\u5ea6\u4e0e\u6a21\u578b\u65b9\u5411\u4e00\u81f4':'\u672a\u5927\u5e45\u504f\u79bb\uff0c\u5e02\u573a\u9884\u671f\u5408\u7406');
        if(scType)cl+='\u3002\u8d5b\u4e8b\u7c7b\u578b\u300c'+scType+'\u300d\uff0c\u6846\u67b6\u8be5\u573a\u666f\u4e0b\u7f6e\u4fe1\u5ea6\u6b63\u5e38\u3002';
        cl+='\u65b9\u5411\u5224\u65ad\u6b63\u786e\uff0c\u56e0\u5b50\u4fee\u6b63\u4e0eDDI\u6821\u51c6\u672a\u51fa\u73b0\u7cfb\u7edf\u6027\u504f\u5dee\u3002';
      }else{
        cl='\u6846\u67b6\u504f\u5dee\u5206\u6790\uff1a';
        if(Math.abs(lambdaD)<0.5)cl+='\u03bb\u5dee\u5f02\u5ea6\u4ec5'+lambdaD.toFixed(3)+'\uff08\u6a21\u578b\u533a\u5206\u5ea6\u4e0d\u8db3\uff09\uff0c';
        else cl+='\u03bb\u5dee\u5f02\u5ea6'+lambdaD.toFixed(3)+'\uff08\u6a21\u578b\u6709\u533a\u5206\u4f46\u65b9\u5411\u504f\u79bb\uff09\uff0c';
        if(scType)cl+='\u8d5b\u4e8b\u7c7b\u578b\u300c'+scType+'\u300d\uff0c\u53ef\u80fd\u4e3a\u6846\u67b6\u76f2\u533a\u573a\u666f\u3002';
        var parts=diag?diag.split(' '):[];
        if(parts.length>=4&&parts[0]==='pred')cl+='\u9884\u6d4b\u300c'+parts[1]+'\u300d\u504f\u79bb\u5b9e\u9645\u300c'+parts[3]+'\u300d\u3002';
        else cl+='\u9884\u6d4b\u65b9\u5411\u4e0e\u5b9e\u9645\u8d5b\u679c\u4e0d\u7b26\u3002';
        cl+='\u5efa\u8bae\uff1a\u68c0\u67e5lambda\u539f\u59cb\u503c\u8ba1\u7b97\u3001\u4f24\u75c5/\u6218\u610f\u4fee\u6b63\u5e45\u5ea6\u662f\u5426\u8fc7\u6fc0\u3001DDI\u6821\u51c6\u662f\u5426\u4e0e\u57fa\u672c\u9762\u80cc\u79bb\u3002';
      }
      dh+='<div class="ana-i" style="grid-column:1/-1;background:var(--surface)"><span class="ana-l">复盘结论</span><span style="line-height:1.8;font-size:12px">'+cl+'</span></div>';
      h+='<div class="cd"><div class="ana">'+dh+'</div></div>';
      h+='</div>';
    });
  }else{
    h+='<div style="text-align:center;padding:30px 0;color:var(--t3);font-size:12px">暂无昨日扫盘数据</div>';
  }


  document.getElementById('rv').innerHTML=h;
  document.querySelectorAll('#rv .card').forEach(function(c){
    c.addEventListener('click',function(){
      var e=this.classList.contains('expanded');
      document.querySelectorAll('#rv .card.expanded').forEach(function(x){x.classList.remove('expanded');});
      if(!e){this.classList.add('expanded');}
    });
  });
}

window.onload=function(){
  fetch('/api/latest').then(function(r){return r.json();}).then(function(d){
    if(d.rating&&d.rating.length>0)rs(d);
  }).catch(function(){});
};
