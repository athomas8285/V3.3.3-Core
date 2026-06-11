
(function(){
  var lw=document.getElementById('liveWrap'),lp=document.getElementById('livePanel'),lt,lo=false;
  lw.addEventListener('mouseenter',function(){clearTimeout(lt);lp.classList.add('open');});
  lw.addEventListener('mouseleave',function(){lt=setTimeout(function(){lp.classList.remove('open');},100);});
  lp.addEventListener('mouseenter',function(){clearTimeout(lt);lp.classList.add('open');});
  lp.addEventListener('mouseleave',function(){lt=setTimeout(function(){lp.classList.remove('open');},100);});
  lw.querySelector('button').addEventListener('click',function(e){e.stopPropagation();lo=!lo;lp.classList.toggle('open',lo);clearTimeout(lt);});
  document.addEventListener('click',function(e){if(!lp.contains(e.target)&&!lw.contains(e.target)&&lo){lo=false;lp.classList.remove('open');}});
  
  function loadLiveInfo() {
    var body=document.getElementById('livePanelBody');
    body.innerHTML='<div class="loading">加载中...</div>';
    fetch('/api/live/info').then(function(r){return r.json();}).then(function(data){
      if(!data.matches||data.matches.length===0){
        body.innerHTML='<div style="text-align:center;padding:30px;color:var(--t3);font-size:12px">暂无赛事数据</div>';
        return;
      }
      var h='';
      data.matches.forEach(function(m){
        var initSP=m.init_sp_home+'/'+m.init_sp_draw+'/'+m.init_sp_away;
        h+='<div class="meth" style="margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--bd)">';
        h+='<div class="meth-h">#'+m.id+' '+m.home+' vs '+m.away+'</div>';
        h+='<div style="font-size:10px;color:var(--t3);margin:2px 0 6px">'+m.event+' '+m.time.slice(5,16)+' | 初始SP: '+initSP+'</div>';
        h+='<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;margin-bottom:6px">';
        h+='<div><label style="font-size:10px;color:var(--t3)">主胜SP</label><br><input id="sp_h_'+m.id+'" value="'+m.sp_home+'" style="width:100%;padding:3px 6px;border:1px solid var(--bd);border-radius:3px;font-family:var(--mono);font-size:12px;background:var(--surface)"></div>';
        h+='<div><label style="font-size:10px;color:var(--t3)">平局SP</label><br><input id="sp_d_'+m.id+'" value="'+m.sp_draw+'" style="width:100%;padding:3px 6px;border:1px solid var(--bd);border-radius:3px;font-family:var(--mono);font-size:12px;background:var(--surface)"></div>';
        h+='<div><label style="font-size:10px;color:var(--t3)">客胜SP</label><br><input id="sp_a_'+m.id+'" value="'+m.sp_away+'" style="width:100%;padding:3px 6px;border:1px solid var(--bd);border-radius:3px;font-family:var(--mono);font-size:12px;background:var(--surface)"></div>';
        h+='</div>';
        h+='<div id="live_result_'+m.id+'"></div>';
        h+='<div style="margin-top:4px;display:flex;gap:4px">';
        h+='<button onclick="doLiveRecalibrate(\''+m.id+'\')" style="flex:1;background:var(--green);color:#fff;border:none;padding:4px 8px;border-radius:3px;font-size:11px;cursor:pointer">重新校准</button>';
        h+='<button onclick="setLineup(\''+m.id+'\',true)" style="background:#eef2f7;color:var(--ink);border:1px solid var(--bd);padding:4px 8px;border-radius:3px;font-size:11px;cursor:pointer">首发确认</button>';
        h+='<button onclick="setLineup(\''+m.id+'\',false)" style="background:#f5ecec;color:var(--red);border:1px solid var(--bd);padding:4px 8px;border-radius:3px;font-size:11px;cursor:pointer">核心缺阵</button>';
        h+='</div></div>';
      });
      h+='<button onclick="doBatchRecalibrate()" style="width:100%;background:var(--ink);color:#f5f4ed;border:none;padding:6px;border-radius:4px;font-size:12px;cursor:pointer;margin-top:4px">批量校准</button>';
      body.innerHTML=h;
    }).catch(function(){
      body.innerHTML='<div style="text-align:center;padding:30px;color:var(--red);font-size:12px">加载失败</div>';
    });
  }
  
  window.doLiveRecalibrate = function(mid) {
    var sh=parseFloat(document.getElementById('sp_h_'+mid).value);
    var sd=parseFloat(document.getElementById('sp_d_'+mid).value);
    var sa=parseFloat(document.getElementById('sp_a_'+mid).value);
    fetch('/api/live/recalibrate',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({matches:[{mid:mid,sp_home:sh,sp_draw:sd,sp_away:sa}]})
    }).then(function(r){return r.json();}).then(function(data){
      var result=data.results&&data.results[0];
      if(!result||result.error){
        document.getElementById('live_result_'+mid).innerHTML='<div style="color:var(--red);font-size:11px">错误: '+(result?result.error:'未知')+'</div>';
        return;
      }
      var b=result.before,a=result.after;
      var fitDelta=(a.fit_score-b.fit_score).toFixed(1);
      var ddiH=a.ddi_change.home_win;
      var html='<div style="background:var(--surface-2);border-radius:4px;padding:6px 8px;font-size:11px;line-height:1.6">';
      html+='<div style="display:flex;justify-content:space-between;font-weight:600;color:var(--t2);border-bottom:1px solid var(--bd);padding-bottom:3px;margin-bottom:3px"><span>校准前</span><span>校准后</span></div>';
      html+='<div style="display:flex;justify-content:space-between"><span>方向</span><span>'+b.方向+'</span><span>'+a.方向+'</span></div>';
      html+='<div style="display:flex;justify-content:space-between"><span>适配度</span><span>'+b.fit_score.toFixed(1)+'</span><span>'+a.fit_score.toFixed(1)+' ('+(fitDelta>0?'+':'')+fitDelta+')</span></div>';
      html+='<div style="display:flex;justify-content:space-between"><span>评级</span><span>'+b.rating+'</span><span>'+a.rating+'</span></div>';
      html+='<div style="display:flex;justify-content:space-between"><span>DDI主胜</span><span>'+ddiH.old.toFixed(4)+'</span><span>'+ddiH.new.toFixed(4)+' ('+(ddiH.delta>0?'+':'')+ddiH.delta.toFixed(4)+')</span></div>';
      html+='<div style="margin-top:4px;font-size:10px;color:var(--t3)">SP: '+a.sp.home+'/'+a.sp.draw+'/'+a.sp.away+' | P: '+(a.p_market.home_win*100).toFixed(1)+'/'+(a.p_market.draw*100).toFixed(1)+'/'+(a.p_market.away_win*100).toFixed(1)+'%</div>';
      if(a.lineup_bonus!=0) html+='<div style="margin-top:2px;font-size:10px;color:var(--'+(a.lineup_bonus>0?'green':'red')+')">lineup: '+(a.lineup_bonus>0?'+'+a.lineup_bonus:a.lineup_bonus)+'</div>';
      html+='</div>';
      document.getElementById('live_result_'+mid).innerHTML=html;
    }).catch(function(){
      document.getElementById('live_result_'+mid).innerHTML='<div style="color:var(--red);font-size:11px">请求失败</div>';
    });
  };
  
  window.setLineup = function(mid, confirmed) {
    var sh=parseFloat(document.getElementById('sp_h_'+mid).value);
    var sd=parseFloat(document.getElementById('sp_d_'+mid).value);
    var sa=parseFloat(document.getElementById('sp_a_'+mid).value);
    fetch('/api/live/recalibrate',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({matches:[{mid:mid,sp_home:sh,sp_draw:sd,sp_away:sa,lineup_confirmed:confirmed}]})
    }).then(function(r){return r.json();}).then(function(data){
      var result=data.results&&data.results[0];
      if(result&&!result.error){
        var a=result.after;
        var fitDelta=(a.fit_score-result.before.fit_score).toFixed(1);
        var html='<div style="background:var(--surface-2);border-radius:4px;padding:6px 8px;font-size:11px;line-height:1.6">';
        html+='<div style="color:var(--green);font-weight:600;margin-bottom:3px">'+(confirmed?'首发已确认':'key out')+'</div>';
        html+='<div><span>fit: </span><span>'+result.before.fit_score.toFixed(1)+' &rarr; '+a.fit_score.toFixed(1)+' ('+(fitDelta>0?'+':'')+fitDelta+')</span></div>';
        html+='<div><span>rating: </span><span>'+result.before.rating+' &rarr; '+a.rating+'</span></div>';
        html+='</div>';
        document.getElementById('live_result_'+mid).innerHTML=html;
      }
    });
  };
  
  window.doBatchRecalibrate = function() {
    var matches=[];
    document.querySelectorAll('#livePanelBody input').forEach(function(inp){
      var id=inp.id;
      if(id.startsWith('sp_h_')) matches.push(id.replace('sp_h_',''));
    });
    var payload={matches:[]};
    matches.forEach(function(mid){
      payload.matches.push({
        mid:mid,
        sp_home:parseFloat(document.getElementById('sp_h_'+mid).value),
        sp_draw:parseFloat(document.getElementById('sp_d_'+mid).value),
        sp_away:parseFloat(document.getElementById('sp_a_'+mid).value)
      });
    });
    fetch('/api/live/recalibrate',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(payload)
    }).then(function(r){return r.json();}).then(function(data){
      data.results.forEach(function(r){
        if(r&&!r.error) window.doLiveRecalibrate(r.match_id);
      });
    });
  };
  
  var loaded=false;
  lw.addEventListener('mouseenter',function(){if(!loaded){loaded=true;loadLiveInfo();}});
  lp.addEventListener('mouseenter',function(){if(!loaded){loaded=true;loadLiveInfo();}});
})();
