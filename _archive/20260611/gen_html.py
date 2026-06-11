import os

html = []
html.append('<!DOCTYPE html>')
html.append('<html lang="zh-CN">')
html.append('<head><meta charset=UTF-8><title>V3.3.3-Core</title><style>')
html.append('*{margin:0;padding:0}')
html.append('body{font-family:sans-serif;background:#0f0c29;color:#e0e0e0;padding:20px}')
html.append('h1{text-align:center;color:#e94560}')
html.append('table{width:100%;border-collapse:collapse;background:#16213e;border-radius:8px;overflow:hidden}')
html.append('th{background:#0f3460;padding:8px 6px;text-align:left;font-size:12px}')
html.append('td{padding:8px 6px;border-bottom:1px solid #1a1a2e;font-size:13px}')
html.append('tr:hover td{background:rgba(255,255,255,0.03)}')
html.append('.detail-row{display:none}.detail-row.show{display:table-row}')
html.append('.detail-box{padding:12px 16px;background:rgba(15,52,96,0.3);font-size:12px;line-height:1.7}')
html.append('.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:bold}')
html.append('.badge-s{background:rgba(13,71,161,0.3);color:#64b5f6}')
html.append('.badge-a{background:rgba(230,81,0,0.3);color:#ffab40}')
html.append('.badge-b{background:rgba(46,125,50,0.3);color:#81c784}')
html.append('.badge-c{background:rgba(120,120,120,0.3);color:#aaa}')
html.append('.chart-box{flex:1;min-width:240px;background:rgba(0,0,0,0.25);border-radius:8px;padding:10px;margin:4px}')
html.append('.chart-title{font-size:12px;color:#e0e0e0;margin-bottom:6px}')
html.append('.ddi-pos{color:#66bb6a}.ddi-neg{color:#ef5350}')
html.append('</style></head><body><div style=max-width:1400px;margin:0 auto>')
html.append('<h1>V3.3.3-Core \u8db3\u7403\u91cf\u5316\u5206\u6790\u7cfb\u7edf</h1>')
html.append('<div id=r></div></div>')

# JS
js = []
js.append('function bg(r,f){')
js.append("if(r==='S')return'<span class=badge badge-s>S\u7ea7</span>'")
js.append("if(r==='A')return'<span class=badge badge-a>A\u7ea7</span>'")
js.append("if(r==='C')return'<span class=badge badge-c>C\u7ea7</span>'")
js.append('if(f>=9)return\'<span class=badge badge-s>S\u7ea7</span>\'')
js.append('if(f>=7)return\'<span class=badge badge-a>A\u7ea7</span>\'')
js.append('if(f>=5)return\'<span class=badge badge-b>B\u7ea7</span>\'')
js.append('return\'<span class=badge badge-c>C\u7ea7</span>\'}')

js.append('function sw(n){')
js.append("document.getElementById('r').addEventListener('click',function(e){")
js.append("var tr=e.target.closest('tr[data-did]');if(tr){var id=tr.getAttribute('data-did');var dt=document.getElementById(id);if(dt)dt.classList.toggle('show')}")
js.append('})}')

# ---- SVG Chart Functions ----
# Lambda chart
js.append('function lambdaChart(lh,la,ld,ddi){')
js.append('var M=Math.max(lh,la,1.5)*1.3,bW=50,g=30,cH=100,cY=30,W=260,H=140')
js.append('var s=\'<svg width="\'+W+\'" height="\'+H+\'" xmlns="http://www.w3.org/2000/svg">\'')
js.append('for(var i=0;i<=4;i++){var v=(M/4)*i,y=cY+cH-(v/M)*cH')
js.append("s+='<line x1=40 y1='+y+' x2='+(W-10)+' y2='+y+' stroke=rgba(255,255,255,0.1) stroke-width=0.5/>'")
js.append("s+='<text x=35 y='+(y+3)+' fill=#888 font-size=9 text-anchor=end>'+v.toFixed(1)+'</text>'}")
js.append('var bX=(W-bW*2-g)/2')
# home bar
js.append('var bH=Math.max((lh/M)*cH,2)')
js.append("s+='<rect x='+bX+' y='+(cY+cH-bH)+' width='+bW+' height='+bH+' rx=3 fill=#66bb6a opacity=0.85/>'")
js.append("s+='<text x='+(bX+bW/2)+' y='+(cY+cH-bH-5)+' fill=#fff font-size=11 font-weight=bold text-anchor=middle>'+lh.toFixed(3)+'</text>'")
js.append("s+='<text x='+(bX+bW/2)+' y='+(cY+cH+14)+' fill=#999 font-size=9 text-anchor=middle>\u03bb\u4e3b</text>'")
# away bar
js.append('var bX2=bX+bW+g,bH2=Math.max((la/M)*cH,2)')
js.append("s+='<rect x='+bX2+' y='+(cY+cH-bH2)+' width='+bW+' height='+bH2+' rx=3 fill=#ef5350 opacity=0.85/>'")
js.append("s+='<text x='+(bX2+bW/2)+' y='+(cY+cH-bH2-5)+' fill=#fff font-size=11 font-weight=bold text-anchor=middle>'+la.toFixed(3)+'</text>'")
js.append("s+='<text x='+(bX2+bW/2)+' y='+(cY+cH+14)+' fill=#999 font-size=9 text-anchor=middle>\u03bb\u5ba2</text>'")
# DDI display
js.append("var ddiC=ddi>0.05?'#ef5350':'#66bb6a'")
js.append("s+='<text x=40 y=16 fill=#ffa726 font-size=11 font-weight=bold>\u03bb\u5dee\u503c: '+ld.toFixed(3)+'</text>'")
js.append("s+='<text x=40 y='+(cY+cH+30)+' fill='+ddiC+' font-size=10>DDI '+(ddi>=0?'+':'')+ddi.toFixed(3)+'</text>'")
js.append("s+='</svg>'")
js.append("return'<div class=chart-box><div class=chart-title>\u03bb\u5bf9\u6bd4 \u00b7 DDI</div>'+s+'</div>'")
js.append('}')

# Probability comparison chart
js.append('function probChart(phys,mkt,ddi){')
js.append('var bW=30,bG=4,gW=bW*2+bG,W=260,H=150,cH=100,cY=30')
js.append('var groups=[[\u4e3b\u80dc,phys.home_win||0,mkt.home_win||0,ddi.home_win||0],[\u5e73\u5c40,phys.draw||0,mkt.draw||0,ddi.draw||0],[\u5ba2\u80dc,phys.away_win||0,mkt.away_win||0,ddi.away_win||0]]')
js.append('var maxP=0;groups.forEach(function(g){maxP=Math.max(maxP,g[1],g[2])});maxP=Math.ceil(maxP*100/5)*5+5;maxP=Math.max(maxP,55)')
js.append("var s='<svg width="'+W+'" height="'+H+'" xmlns="http://www.w3.org/2000/svg">'")
# Grid
js.append('for(var p=0;p<=maxP;p+=10){var y=cY+cH-(p/maxP)*cH')
js.append("s+='<line x1=38 y1='+y+' x2='+(W-10)+' y2='+y+' stroke=rgba(255,255,255,0.1) stroke-width=0.5/>'")
js.append("s+='<text x=33 y='+(y+3)+' fill=#888 font-size=9 text-anchor=end>'+p+'%</text>'}")
# Bars
js.append('var gap=8,totalW=groups.length*(bW*2+bG)+gap*2,startX=38+(W-38-10-totalW)/2')
js.append('groups.forEach(function(g,i){var x=startX+i*((bW*2+bG)+gap)')
# Physical bar (blue)
js.append('var b1=Math.max((g[1]/maxP)*cH,2)')
js.append("s+='<rect x='+x+' y='+(cY+cH-b1)+' width='+bW+' height='+b1+' rx=2 fill=#42a5f5 opacity=0.85/>'")
js.append("s+='<text x='+(x+bW/2)+' y='+(cY+cH-b1-3)+' fill=#e0e0e0 font-size=9 font-weight=bold text-anchor=middle>'+(g[1]*100).toFixed(1)+'%</text>'")
# Market bar (red)
js.append('var x2=x+bW+bG,b2=Math.max((g[2]/maxP)*cH,2)')
js.append("s+='<rect x='+x2+' y='+(cY+cH-b2)+' width='+bW+' height='+b2+' rx=2 fill=#ef5350 opacity=0.85/>'")
js.append("s+='<text x='+(x2+bW/2)+' y='+(cY+cH-b2-3)+' fill=#e0e0e0 font-size=9 font-weight=bold text-anchor=middle>'+(g[2]*100).toFixed(1)+'%</text>'")
# Group label
js.append("s+='<text x='+(x+bW+bG/2+bW/2)+' y='+(cY+cH+14)+' fill=#aaa font-size=10 text-anchor=middle>'+g[0]+'</text>'")
# DDI value
js.append("var dv=g[3];var dc=Math.abs(dv)>0.05?'#ef5350':'#66bb6a'")
js.append("s+='<text x='+(x+bW+bG/2+bW/2)+' y='+(cY+cH+26)+' fill='+dc+' font-size=8 text-anchor=middle>DDI '+(dv>=0?'+':'')+dv.toFixed(3)+'</text>'")
# Highlight gap for home win (first group)
js.append("if(i===0&&Math.abs(g[1]-g[2])>0.05){")
js.append("var midX=x+bW+bG/2+bW/2,arrowY=cY+cH-Math.max(b1,b2)-10")
js.append("s+='<text x='+midX+' y='+arrowY+' fill=#ff5252 font-size=9 font-weight=bold text-anchor=middle>\u25bc '+((g[1]-g[2])*100).toFixed(1)+'%</text>'")
js.append('}')

js.append('})')
# Legend
js.append("s+='<text x='+(W-120)+' y=16 fill=#42a5f5 font-size=9>\u25a0 \u7269\u7406</text>'")
js.append("s+='<text x='+(W-50)+' y=16 fill=#ef5350 font-size=9>\u25a0 \u5e02\u573a</text>'")
js.append("s+='</svg>'")
js.append("return'<div class=chart-box><div class=chart-title>\u7269\u7406\u6982\u7387 vs \u5e02\u573a\u6982\u7387</div>'+s+'</div>'")
js.append('}')

# Main render
js.append('function rs(d){')
js.append('var r=d.rating,mi=d.info||[],dd=d.ddi||[],ai=d.ai||[],mc=d.mc||[]')
js.append('var im={},dm={},am={},mm={}')
js.append('mi.forEach(function(m){im[m.id]=m})')
js.append('dd.forEach(function(m){dm[m.id]=m})')
js.append('ai.forEach(function(m){am[m.id]=m})')
js.append('mc.forEach(function(m){mm[m.id]=m})')
js.append('var s=[].concat(r).sort(function(a,b){return a.id.localeCompare(b.id)})')
js.append("var h='<table><thead><tr><th>\u7f16\u53f7</th><th>\u65f6\u95f4</th><th>\u5bf9\u9635</th><th>\u65b9\u5411</th><th>\u6982\u7387</th><th>\u03bb</th><th>DDI</th><th>S7</th><th>\u76d8\u53e3</th><th>\u8bc4\u5206</th><th>\u8bc4\u7ea7</th><th></th></tr></thead><tbody>'")

js.append('s.forEach(function(x){')
js.append('var m=im[x.id]||{},mc2=mm[x.id]||{},dr=dm[x.id]||{},ar=am[x.id]||{}')
js.append('var p=mc2.physical||{}')
js.append('var hw=(p.home_win||0)*100,dw=(p.draw||0)*100,aw=(p.away_win||0)*100')
js.append('var dh=(dr.ddi||{}).home_win||0,s7=ar.s7_score||0')
js.append('var lh=mc2.lambda_h_final||0,la=mc2.lambda_a_final||0')
js.append('var ah=m.asian_handicap||0')
js.append("var hs=ah===0?'0':(ah>0?'+'+ah.toFixed(1):ah.toFixed(1))")
js.append("var tm=m.time||'',ko=tm.length>=16?tm.substring(5,10)+'/'+tm.substring(11,16):''")
js.append("var did='d'+x.id")
# Prob bar
js.append("var pb='<div>'+Math.round(hw)+'/'+Math.round(dw)+'/'+Math.round(aw)+'</div>'")
js.append("pb+=\"<div style='display:flex;height:12px;background:rgba(255,255,255,0.1);border-radius:4px;overflow:hidden;margin-top:2px'>\"")
js.append("pb+=\"<div style='height:100%;background:#66bb6a;width:\"+hw+\"%'></div>\"")
js.append("pb+=\"<div style='height:100%;background:#ffa726;width:\"+dw+\"%'></div>\"")
js.append("pb+=\"<div style='height:100%;background:#ef5350;width:\"+aw+\"%'></div>\"")
js.append("pb+='</div>'")
js.append("var ds='<span>'+(dh>=0?'+'+dh.toFixed(3):dh.toFixed(3))+'</span>'")
js.append("var ss=s7>0?'<span>'+s7+'</span>':'<span>0</span>'")

# Row
js.append("h+='<tr data-did='+did+'>'")
js.append("h+='<td>'+x.id+'</td><td>'+ko+'</td><td>'+x.home+' vs '+x.away+'</td>'")
js.append("h+='<td><b>'+x.direction+'</b></td><td>'+pb+'</td>'")
js.append("h+='<td>'+lh.toFixed(2)+'/'+la.toFixed(2)+'</td>'")
js.append("h+='<td>'+ds+'</td><td>'+ss+'</td><td>'+hs+'</td>'")
js.append("h+='<td>'+x.fit_score.toFixed(1)+'</td>'")
js.append("h+='<td>'+bg(x.rating,x.fit_score)+'</td>'")
js.append("h+='<td>\u25bc</td></tr>'")

# Detail row
js.append("var trap=ar.trap_analysis||'',risk=ar.key_risk||'',s7r=ar.s7_reason||'',ld=mc2.lambda_diff||0")
js.append("var ddi_a=dr.ddi||{home_win:0,draw:0,away_win:0}")
js.append("h+='<tr class=detail-row id='+did+'><td colspan=12><div class=detail-box>'")
js.append("h+='<b>\u03bb\u5dee\u503c:</b> '+ld.toFixed(3)")
js.append("if(s7r)h+='<br><b>S7\u8bf4\u660e:</b> '+s7r")
js.append("if(trap)h+='<br><b>\u8bf1\u76d8\u5206\u6790:</b> '+trap")
js.append("if(risk)h+='<br><b style=color:#ef5350>\u98ce\u9669\u63d0\u793a:</b> '+risk")

# Charts container
js.append("h+='<div style=display:flex;gap:12px;flex-wrap:wrap;margin-top:10px>'")
js.append("h+=lambdaChart(lh,la,ld,dh)")
js.append("h+=probChart(p,dr.p_market||{},ddi_a)")
js.append("h+='</div>'")

js.append("h+='</div></td></tr>'")
js.append('})')
js.append("h+='</tbody></table>'")
js.append("document.getElementById('r').innerHTML=h")
js.append('}')

js.append("window.onload=function(){fetch('/api/latest').then(function(r){return r.json();}).then(function(d){if(d.rating&&d.rating.length>0)rs(d)}).catch(function(){})}")
js.append("</script></body></html>")

html.append('<script>')
for j in js:
    html.append(j)
html.append('</script></body></html>')

with open('C:/Users/gjj/Desktop/v333/templates/index.html','w',encoding='utf-8') as f:
    f.write('\n'.join(html))
print('OK:',len('\n'.join(html)))
