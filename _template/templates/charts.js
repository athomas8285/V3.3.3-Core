var _DATA = null;

function bg(r, f) {
  if (r === 'S') return '<span class="badge badge-s">S级</span>';
  if (r === 'A') return '<span class="badge badge-a">A级</span>';
  if (r === 'C') return '<span class="badge badge-c">C级</span>';
  if (f >= 9) return '<span class="badge badge-s">S级</span>';
  if (f >= 7) return '<span class="badge badge-a">A级</span>';
  if (f >= 5) return '<span class="badge badge-b">B级</span>';
  return '<span class="badge badge-c">C级</span>';
}

function buildCharts() {
  if (!_DATA) return;
  var NS = 'http://www.w3.org/2000/svg';
  var ratings = _DATA.rating || [];
  var mcs = _DATA.mc || [];
  var ddis = _DATA.ddi || [];

  document.querySelectorAll('tr[data-did]').forEach(function (tr) {
    var id = tr.getAttribute('data-did');
    var matchId = id.replace(/^d/, '');
    // find matching index
    var idx = -1;
    for (var i = 0; i < ratings.length; i++) {
      if (ratings[i].id === matchId) { idx = i; break; }
    }
    if (idx < 0) return;
    var mc = mcs[idx] || {};
    var dd = ddis[idx] || {};

    var mcPhysical = mc.physical || {};
    var phw = mcPhysical.home_win || 0;
    var pdw = mcPhysical.draw || 0;
    var paw = mcPhysical.away_win || 0;

    var marketProb = dd.p_market || {};
    var mhw = marketProb.home_win || 0;
    var mdw = marketProb.draw || 0;
    var maw = marketProb.away_win || 0;

    var ddiObj = dd.ddi || {};
    var ddiHome = ddiObj.home_win || 0;

    var lh = mc.lambda_h_final || 0;
    var la = mc.lambda_a_final || 0;
    var ld = mc.lambda_diff || (lh - la);

    var detail = document.getElementById(id);
    if (!detail) return;
    var db = detail.querySelector('.detail-box');
    if (!db) return;

    var chartDiv = document.createElement('div');
    chartDiv.style.cssText = 'display:flex;gap:12px;flex-wrap:wrap;margin-top:10px';

    // ---- Chart 1: Lambda bar + DDI ----
    var c1 = document.createElement('div');
    c1.className = 'cb';
    var t1 = document.createElement('div');
    t1.className = 'ct';
    t1.textContent = 'λ对比 · DDI';
    c1.appendChild(t1);

    var svg1 = document.createElementNS(NS, 'svg');
    svg1.setAttribute('width', '260');
    svg1.setAttribute('height', '140');
    svg1.setAttribute('viewBox', '0 0 260 140');

    var maxVal = Math.max(lh, la, 1.5) * 1.3;
    var bW = 50, gap = 30, cH = 100, cY = 30;
    var bX = (260 - bW * 2 - gap) / 2;

    // grid lines
    for (var gi = 0; gi <= 4; gi++) {
      var v = (maxVal / 4) * gi;
      var y = cY + cH - (v / maxVal) * cH;
      var line = document.createElementNS(NS, 'line');
      line.setAttribute('x1', '40'); line.setAttribute('y1', y);
      line.setAttribute('x2', '250'); line.setAttribute('y2', y);
      line.setAttribute('stroke', 'rgba(255,255,255,0.1)'); line.setAttribute('stroke-width', '0.5');
      svg1.appendChild(line);
      var txt = document.createElementNS(NS, 'text');
      txt.setAttribute('x', '35'); txt.setAttribute('y', y + 3);
      txt.setAttribute('fill', '#888'); txt.setAttribute('font-size', '9'); txt.setAttribute('text-anchor', 'end');
      txt.textContent = v.toFixed(1);
      svg1.appendChild(txt);
    }

    // home bar
    var bH = Math.max((lh / maxVal) * cH, 2);
    var r1 = document.createElementNS(NS, 'rect');
    r1.setAttribute('x', bX); r1.setAttribute('y', cY + cH - bH);
    r1.setAttribute('width', bW); r1.setAttribute('height', bH);
    r1.setAttribute('rx', '3'); r1.setAttribute('fill', '#66bb6a'); r1.setAttribute('opacity', '0.85');
    svg1.appendChild(r1);
    var vl1 = document.createElementNS(NS, 'text');
    vl1.setAttribute('x', bX + bW / 2); vl1.setAttribute('y', cY + cH - bH - 5);
    vl1.setAttribute('fill', '#fff'); vl1.setAttribute('font-size', '11'); vl1.setAttribute('font-weight', 'bold'); vl1.setAttribute('text-anchor', 'middle');
    vl1.textContent = lh.toFixed(3);
    svg1.appendChild(vl1);
    var lb1 = document.createElementNS(NS, 'text');
    lb1.setAttribute('x', bX + bW / 2); lb1.setAttribute('y', cY + cH + 14);
    lb1.setAttribute('fill', '#999'); lb1.setAttribute('font-size', '9'); lb1.setAttribute('text-anchor', 'middle');
    lb1.textContent = 'λ主';
    svg1.appendChild(lb1);

    // away bar
    var bX2 = bX + bW + gap;
    var bH2 = Math.max((la / maxVal) * cH, 2);
    var r2 = document.createElementNS(NS, 'rect');
    r2.setAttribute('x', bX2); r2.setAttribute('y', cY + cH - bH2);
    r2.setAttribute('width', bW); r2.setAttribute('height', bH2);
    r2.setAttribute('rx', '3'); r2.setAttribute('fill', '#ef5350'); r2.setAttribute('opacity', '0.85');
    svg1.appendChild(r2);
    var vl2 = document.createElementNS(NS, 'text');
    vl2.setAttribute('x', bX2 + bW / 2); vl2.setAttribute('y', cY + cH - bH2 - 5);
    vl2.setAttribute('fill', '#fff'); vl2.setAttribute('font-size', '11'); vl2.setAttribute('font-weight', 'bold'); vl2.setAttribute('text-anchor', 'middle');
    vl2.textContent = la.toFixed(3);
    svg1.appendChild(vl2);
    var lb2 = document.createElementNS(NS, 'text');
    lb2.setAttribute('x', bX2 + bW / 2); lb2.setAttribute('y', cY + cH + 14);
    lb2.setAttribute('fill', '#999'); lb2.setAttribute('font-size', '9'); lb2.setAttribute('text-anchor', 'middle');
    lb2.textContent = 'λ客';
    svg1.appendChild(lb2);

    var title1 = document.createElementNS(NS, 'text');
    title1.setAttribute('x', '40'); title1.setAttribute('y', '16');
    title1.setAttribute('fill', '#ffa726'); title1.setAttribute('font-size', '11'); title1.setAttribute('font-weight', 'bold');
    title1.textContent = 'λ差值: ' + ld.toFixed(3);
    svg1.appendChild(title1);

    var dc = Math.abs(ddiHome) > 0.05 ? '#ef5350' : '#66bb6a';
    var ddiEl = document.createElementNS(NS, 'text');
    ddiEl.setAttribute('x', '40'); ddiEl.setAttribute('y', cY + cH + 30);
    ddiEl.setAttribute('fill', dc); ddiEl.setAttribute('font-size', '10');
    ddiEl.textContent = 'DDI ' + (ddiHome >= 0 ? '+' : '') + ddiHome.toFixed(3);
    svg1.appendChild(ddiEl);

    c1.appendChild(svg1);
    chartDiv.appendChild(c1);

    // ---- Chart 2: Physical vs Market probability ----
    var c2 = document.createElement('div');
    c2.className = 'cb';
    var t2 = document.createElement('div');
    t2.className = 'ct';
    t2.textContent = '物理概率 vs 市场概率';
    c2.appendChild(t2);

    var svg2 = document.createElementNS(NS, 'svg');
    svg2.setAttribute('width', '260');
    svg2.setAttribute('height', '150');
    svg2.setAttribute('viewBox', '0 0 260 150');

    var barW = 30, barG = 4, cH2 = 100, cY2 = 30;
    var groups = [
      ['主胜', phw, mhw, ddiHome],
      ['平局', pdw, mdw, 0],
      ['客胜', paw, maw, -ddiHome]
    ];
    var maxP = 1;
    groups.forEach(function (g) { maxP = Math.max(maxP, g[1], g[2]); });
    maxP = Math.ceil(maxP * 100 / 5) * 5 + 5;
    maxP = Math.max(maxP, 55);
    maxP = maxP / 100;

    // grid
    for (var pi = 0; pi <= maxP * 100; pi += 10) {
      var y2 = cY2 + cH2 - (pi / 100 / maxP) * cH2;
      var ln = document.createElementNS(NS, 'line');
      ln.setAttribute('x1', '38'); ln.setAttribute('y1', y2);
      ln.setAttribute('x2', '250'); ln.setAttribute('y2', y2);
      ln.setAttribute('stroke', 'rgba(255,255,255,0.1)'); ln.setAttribute('stroke-width', '0.5');
      svg2.appendChild(ln);
      var tx = document.createElementNS(NS, 'text');
      tx.setAttribute('x', '33'); tx.setAttribute('y', y2 + 3);
      tx.setAttribute('fill', '#888'); tx.setAttribute('font-size', '9'); tx.setAttribute('text-anchor', 'end');
      tx.textContent = pi + '%';
      svg2.appendChild(tx);
    }

    var gap2 = 8, totalW = groups.length * (barW * 2 + barG) + gap2 * 2;
    var startX = 38 + (250 - 38 - totalW) / 2;

    groups.forEach(function (g, idx) {
      var x = startX + idx * ((barW * 2 + barG) + gap2);
      // physical
      var b1 = Math.max((g[1] / maxP) * cH2, 2);
      var rp = document.createElementNS(NS, 'rect');
      rp.setAttribute('x', x); rp.setAttribute('y', cY2 + cH2 - b1);
      rp.setAttribute('width', barW); rp.setAttribute('height', b1);
      rp.setAttribute('rx', '2'); rp.setAttribute('fill', '#42a5f5'); rp.setAttribute('opacity', '0.85');
      svg2.appendChild(rp);
      var tv1 = document.createElementNS(NS, 'text');
      tv1.setAttribute('x', x + barW / 2); tv1.setAttribute('y', cY2 + cH2 - b1 - 3);
      tv1.setAttribute('fill', '#e0e0e0'); tv1.setAttribute('font-size', '9'); tv1.setAttribute('font-weight', 'bold'); tv1.setAttribute('text-anchor', 'middle');
      tv1.textContent = (g[1] * 100).toFixed(1) + '%';
      svg2.appendChild(tv1);

      // market
      var x2 = x + barW + barG;
      var b2 = Math.max((g[2] / maxP) * cH2, 2);
      var rm = document.createElementNS(NS, 'rect');
      rm.setAttribute('x', x2); rm.setAttribute('y', cY2 + cH2 - b2);
      rm.setAttribute('width', barW); rm.setAttribute('height', b2);
      rm.setAttribute('rx', '2'); rm.setAttribute('fill', '#ef5350'); rm.setAttribute('opacity', '0.85');
      svg2.appendChild(rm);
      var tv2 = document.createElementNS(NS, 'text');
      tv2.setAttribute('x', x2 + barW / 2); tv2.setAttribute('y', cY2 + cH2 - b2 - 3);
      tv2.setAttribute('fill', '#e0e0e0'); tv2.setAttribute('font-size', '9'); tv2.setAttribute('font-weight', 'bold'); tv2.setAttribute('text-anchor', 'middle');
      tv2.textContent = (g[2] * 100).toFixed(1) + '%';
      svg2.appendChild(tv2);

      // label
      var gl = document.createElementNS(NS, 'text');
      gl.setAttribute('x', x + barW + barG / 2 + barW / 2); gl.setAttribute('y', cY2 + cH2 + 14);
      gl.setAttribute('fill', '#aaa'); gl.setAttribute('font-size', '10'); gl.setAttribute('text-anchor', 'middle');
      gl.textContent = g[0];
      svg2.appendChild(gl);

      // DDI below
      var dv = g[3];
      var dcol2 = Math.abs(dv) > 0.05 ? '#ef5350' : '#66bb6a';
      var dtxt = document.createElementNS(NS, 'text');
      dtxt.setAttribute('x', x + barW + barG / 2 + barW / 2); dtxt.setAttribute('y', cY2 + cH2 + 26);
      dtxt.setAttribute('fill', dcol2); dtxt.setAttribute('font-size', '8'); dtxt.setAttribute('text-anchor', 'middle');
      dtxt.textContent = 'DDI ' + (dv >= 0 ? '+' : '') + dv.toFixed(3);
      svg2.appendChild(dtxt);

      // gap indicator for home win
      if (idx === 0 && Math.abs(g[1] - g[2]) > 0.02) {
        var midX = x + barW + barG / 2 + barW / 2, arrowY = cY2 + cH2 - Math.max(b1, b2) - 10;
        var arr = document.createElementNS(NS, 'text');
        arr.setAttribute('x', midX); arr.setAttribute('y', arrowY);
        arr.setAttribute('fill', '#ff5252'); arr.setAttribute('font-size', '9'); arr.setAttribute('font-weight', 'bold'); arr.setAttribute('text-anchor', 'middle');
        arr.textContent = '▼ ' + ((g[1] - g[2]) * 100).toFixed(1) + '%';
        svg2.appendChild(arr);
      }
    });

    // legend
    var lg1 = document.createElementNS(NS, 'text');
    lg1.setAttribute('x', '140'); lg1.setAttribute('y', '16');
    lg1.setAttribute('fill', '#42a5f5'); lg1.setAttribute('font-size', '9');
    lg1.textContent = '■ 物理';
    svg2.appendChild(lg1);
    var lg2 = document.createElementNS(NS, 'text');
    lg2.setAttribute('x', '210'); lg2.setAttribute('y', '16');
    lg2.setAttribute('fill', '#ef5350'); lg2.setAttribute('font-size', '9');
    lg2.textContent = '■ 市场';
    svg2.appendChild(lg2);

    c2.appendChild(svg2);
    chartDiv.appendChild(c2);
    db.appendChild(chartDiv);
  });
}

function rs(d) {
  _DATA = d;
  var r = d.rating, mi = d.info || [], dd = d.ddi || [], ai = d.ai || [], mc = d.mc || [];
  var im = {}, dm = {}, am = {}, mm = {};
  mi.forEach(function (m) { im[m.id] = m; });
  dd.forEach(function (m) { dm[m.id] = m; });
  ai.forEach(function (m) { am[m.id] = m; });
  mc.forEach(function (m) { mm[m.id] = m; });
  var s = [].concat(r).sort(function (a, b) { return a.id.localeCompare(b.id); });
  var h = '<table><thead><tr><th>编号</th><th>时间</th><th>对阵</th><th>方向</th><th>概率</th><th>λ</th><th>DDI</th><th>S7</th><th>盘口</th><th>评分</th><th>评级</th><th></th></tr></thead><tbody>';
  s.forEach(function (x) {
    var m = im[x.id] || {}, mc2 = mm[x.id] || {}, dr = dm[x.id] || {}, ar = am[x.id] || {};
    var p = mc2.physical || {};
    var hw = (p.home_win || 0) * 100, dw = (p.draw || 0) * 100, aw = (p.away_win || 0) * 100;
    var dh = (dr.ddi || {}).home_win || 0, s7 = ar.s7_score || 0;
    var lh = mc2.lambda_h_final || 0, la = mc2.lambda_a_final || 0;
    var ah = m.asian_handicap || 0;
    var hs = ah === 0 ? '0' : (ah > 0 ? '+' + ah.toFixed(1) : ah.toFixed(1));
    var tm = m.time || '', ko = tm.length >= 16 ? tm.substring(5, 10) + '/' + tm.substring(11, 16) : '';
    var did = 'd' + x.id;
    var pb = '<div>' + Math.round(hw) + '/' + Math.round(dw) + '/' + Math.round(aw) + '</div>';
    pb += "<div style='display:flex;height:12px;background:rgba(255,255,255,0.1);border-radius:4px;overflow:hidden;margin-top:2px'>";
    pb += "<div style='height:100%;background:#66bb6a;width:" + hw + "%'></div>";
    pb += "<div style='height:100%;background:#ffa726;width:" + dw + "%'></div>";
    pb += "<div style='height:100%;background:#ef5350;width:" + aw + "%'></div></div>";
    var ds = '<span>' + (dh >= 0 ? '+' + dh.toFixed(3) : dh.toFixed(3)) + '</span>';
    var ss = s7 > 0 ? '<span>' + s7 + '</span>' : '<span>0</span>';
    h += '<tr data-did=' + did + '>';
    h += '<td>' + x.id + '</td><td>' + ko + '</td><td>' + x.home + ' vs ' + x.away + '</td>';
    h += '<td><b>' + x.direction + '</b></td><td>' + pb + '</td>';
    h += '<td>' + lh.toFixed(2) + '/' + la.toFixed(2) + '</td>';
    h += '<td>' + ds + '</td><td>' + ss + '</td><td>' + hs + '</td>';
    h += '<td>' + x.fit_score.toFixed(1) + '</td>';
    h += '<td>' + bg(x.rating, x.fit_score) + '</td>';
    h += '<td>&#9660;</td></tr>';
    var trap = ar.trap_analysis || '', risk = ar.key_risk || '', s7r = ar.s7_reason || '', ld = mc2.lambda_diff || 0;
    h += '<tr class=detail-row id=' + did + '><td colspan=12><div class=detail-box>';
    h += '<b>λ差值:</b> ' + ld.toFixed(3);
    if (s7r) h += '<br><b>S7说明:</b> ' + s7r;
    if (trap) h += '<br><b>诱盘分析:</b> ' + trap;
    if (risk) h += '<br><b style=color:#ef5350>风险提示:</b> ' + risk;
    h += '</div></td></tr>';
  });
  h += '</tbody></table>';
  document.getElementById('r').innerHTML = h;
  buildCharts();
  document.getElementById('r').addEventListener('click', function (e) {
    var tr = e.target.closest('tr[data-did]');
    if (tr) {
      var id = tr.getAttribute('data-did');
      var dt = document.getElementById(id);
      if (dt) dt.classList.toggle('show');
    }
  });
}

window.onload = function () {
  fetch('/api/latest').then(function (r) { return r.json(); }).then(function (d) {
    if (d.rating && d.rating.length > 0) rs(d);
  }).catch(function () {});
};
