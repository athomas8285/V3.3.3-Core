// ==================== GLOBALS ====================
const WEEKDAYS = ["??","??","??","??","??","??","??"];
let overviewData = null;
let allMatchesFlat = [];
let currentMatchFilter = "all";
const panelLoaded = {};

// ==================== UTILS ====================
function fmt(v, d) { return (v === null || v === undefined || v === "") ? (d || "-") : v; }
function fmt1(v, d) { if (v === null || v === undefined || v === "") return d || "-"; var n = Number(v); return isNaN(n) ? (d || "-") : n.toFixed(1); }
function rowClass(m) {
  if (m.actual_score) return "row-done";
  if (m.direction) return "row-pred";
  return "row-wait";
}
function dirClass(direction) {
  if (direction === "\u8d1f" || direction === "\u8ba9\u8d1f") return "lose";
  return "dir";
}
function rateClass(rating) {
  if (rating === "C") return "C";
  return "B";
}
function dirBadgeHTML(rating, direction) {
  return '<span class="dir-badge ' + (rating || "") + '">' + fmt(direction, "\u2014") + '</span>';
}
function parseWeekday(mid) {
  for (const wd of WEEKDAYS) { if (mid && mid.startsWith(wd)) return wd; }
  return null;
}

// ==================== SIDEBAR NAV ====================
document.querySelectorAll(".nav-item").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".nav-item").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    document.getElementById("panel-" + btn.dataset.panel).classList.add("active");
    loadPanel(btn.dataset.panel);
  });
});

document.getElementById("collapse-btn").addEventListener("click", () => {
  document.getElementById("sidebar").classList.toggle("collapsed");
  const icon = document.querySelector("#collapse-btn i");
  icon.setAttribute("data-lucide", document.getElementById("sidebar").classList.contains("collapsed") ? "panel-left-open" : "panel-left-close");
  lucide.createIcons();
});

function updateSidebarTime() {
  document.getElementById("sidebar-time").textContent = new Date().toLocaleString("zh-CN", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}
setInterval(updateSidebarTime, 1000);
updateSidebarTime();

// ==================== PANEL LOADERS ====================
async function loadPanel(name) {
  if (panelLoaded[name]) return;
  panelLoaded[name] = true;
  const loaders = { overview, console: loadConsole, matches: loadMatches, prediction: loadPrediction, plans: loadPlans, review: loadReview, system: loadSystem };
  if (loaders[name]) await loaders[name]();
}

// ==================== CHART ====================
function drawTrendChart(canvasId, trend) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || !trend || !trend.length) return;
  const dpr = window.devicePixelRatio || 1;
  const w = canvas.parentElement.clientWidth - 32;
  const h = 140;
  canvas.width = w * dpr;
  canvas.height = h * dpr;
  canvas.style.width = w + "px";
  canvas.style.height = h + "px";
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);
  const pad = { top: 16, right: 24, bottom: 28, left: 40 };
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;
  const stepX = trend.length > 1 ? pw / (trend.length - 1) : pw;

  ctx.strokeStyle = "#e5e7eb";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pad.left, pad.top);
  ctx.lineTo(pad.left, pad.top + ph);
  ctx.lineTo(pad.left + pw, pad.top + ph);
  ctx.stroke();

  ctx.fillStyle = "#9ca3af";
  ctx.font = "10px -apple-system,BlinkMacSystemFont,sans-serif";
  ctx.textAlign = "right";
  for (let i = 0; i <= 4; i++) {
    const y = pad.top + ph * (1 - i / 4);
    ctx.fillText(i * 25 + "%", pad.left - 6, y + 3);
  }

  ctx.strokeStyle = "#2563eb";
  ctx.lineWidth = 2;
  ctx.beginPath();
  trend.forEach((t, i) => {
    const x = pad.left + i * stepX;
    const y = pad.top + ph * (1 - t.rate / 100);
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  });
  ctx.stroke();

  ctx.fillStyle = "#2563eb";
  ctx.textAlign = "center";
  ctx.font = "10px -apple-system,BlinkMacSystemFont,sans-serif";
  trend.forEach((t, i) => {
    const x = pad.left + i * stepX;
    const y = pad.top + ph * (1 - t.rate / 100);
    ctx.beginPath(); ctx.arc(x, y, 3, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = "#9ca3af";
    ctx.fillText(t.label, x, pad.top + ph + 16);
    ctx.fillStyle = "#2563eb";
  });
}

// ==================== 1. OVERVIEW ====================
async function overview() {
  const r = await fetch("/api/dashboard/overview").then(d => d.json());
  overviewData = r;
  const s = r.stats;

  document.getElementById("ov-stats").innerHTML =
    '<div class="stat-card"><div class="num">' + s.total + '</div><div class="label">\u603b\u6bd4\u8d5b</div></div>' +
    '<div class="stat-card"><div class="num green">' + s.scored + '</div><div class="label">\u5df2\u6709\u8d5b\u679c</div></div>' +
    '<div class="stat-card"><div class="num yellow">' + s.predicted + '</div><div class="label">\u5df2\u9884\u6d4b</div></div>' +
    '<div class="stat-card"><div class="num green">' + s.hit + '</div><div class="label">\u547d\u4e2d</div></div>' +
    '<div class="stat-card"><div class="num red">' + s.miss + '</div><div class="label">\u672a\u547d\u4e2d</div></div>' +
    '<div class="stat-card"><div class="num">' + s.hitrate + '%</div><div class="label">\u547d\u4e2d\u7387</div></div>' +
    '<div class="stat-card"><div class="num yellow">' + (r.today_matches ? r.today_matches.length : 0) + '</div><div class="label">\u4eca\u65e5\u6bd4\u8d5b</div></div>';

  document.getElementById("ov-health").innerHTML =
    '<span class="ok">\u7ade\u5f69\u7f51 API \u2713</span>' +
    '<span class="' + (r.health.sp_missing > 0 ? "warn" : "ok") + '">\u8d54\u7387\u7f3a\u5931 ' + r.health.sp_missing + '/' + r.health.total + '</span>' +
    '<span class="warn">SofaScore \u25cb</span>' +
    '<span>\u4f24\u505c\u4fe1\u606f \u2014</span>';

  let recentHTML = "";
  for (const p of (r.recent_predictions || [])) {
    recentHTML += '<div class="pred-item"><span class="teams">' + fmt(p.home) + ' vs ' + fmt(p.away) +
      '</span>' + dirBadgeHTML(p.rating, p.direction) +
      '<span class="fit">\u8d34\u5408 ' + fmt1(p.fit_score, "\u2014") + '</span></div>';
  }
  document.getElementById("ov-recent").innerHTML = recentHTML || '<div class="empty">\u6682\u65e0\u9884\u6d4b\u6570\u636e</div>';
  drawTrendChart("ov-chart", r.hit_trend || []);
  document.getElementById("sidebar-update").textContent = "\u6700\u540e\u66f4\u65b0: " + new Date().toLocaleTimeString("zh-CN");
  lucide.createIcons();
}

// ==================== CONSOLE ====================
async function loadConsole() {
  if (!overviewData) {
    overviewData = await fetch("/api/dashboard/overview").then(d => d.json());
  }
  const r = overviewData;
  const s = r.stats;

  document.getElementById("console-tasks").innerHTML =
    '<div class="task-card" data-nav="matches"><div class="task-num red">' + r.missing_results + '</div><div class="task-label">\u9700\u8865\u8d5b\u679c</div></div>' +
    '<div class="task-card" data-nav="prediction"><div class="task-num yellow">' + (s.total - s.predicted) + '</div><div class="task-label">\u5f85\u9884\u6d4b</div></div>' +
    '<div class="task-card" data-nav="review"><div class="task-num green">' + (s.hit + s.miss) + '</div><div class="task-label">\u53ef\u590d\u76d8</div></div>' +
    '<div class="task-card" data-nav="plans"><div class="task-num gray">' + (r.plan_info ? r.plan_info.plan_count : "\u2014") + '</div><div class="task-label">\u8ba1\u5212\u5355</div></div>';

  document.querySelectorAll("#console-tasks .task-card").forEach(card => {
    card.addEventListener("click", () => {
      document.querySelector('.nav-item[data-panel="' + card.dataset.nav + '"]').click();
    });
  });

  const clog = document.getElementById("console-log");
  function logMsg(msg, color) {
    clog.style.display = "block";
    clog.innerHTML += '<div style="color:' + (color || "#6b7280") + '">[' + new Date().toLocaleTimeString("zh-CN") + '] ' + msg + '</div>';
    clog.scrollTop = clog.scrollHeight;
  }

  document.getElementById("btn-fetch-results").onclick = async () => {
    logMsg("\u6b63\u5728\u67e5\u8be2\u8d5b\u679c...", "#2563eb");
    try { const d = await fetch("/api/dashboard/action/fetch_results").then(r => r.json()); logMsg(d.msg || "\u67e5\u8be2\u5b8c\u6210", "#16a34a"); }
    catch(e) { logMsg("\u67e5\u8be2\u5931\u8d25: " + e.message, "#dc2626"); }
  };
  document.getElementById("btn-manual-entry").onclick = () => {
    logMsg("\u8bf7\u5728\u6bd4\u8d5b\u6a21\u5757\u4e2d\u624b\u52a8\u7f16\u8f91\u6bd4\u5206\u548c\u534a\u5168\u573a", "#d97706");
    document.querySelector('.nav-item[data-panel="matches"]').click();
  };
  document.getElementById("btn-fetch-jczq").onclick = async () => {
    logMsg("\u6b63\u5728\u4ece\u7ade\u5f69\u7f51\u83b7\u53d6\u6bd4\u8d5b...", "#2563eb");
    try { const d = await fetch("/api/dashboard/action/fetch_jczq").then(r => r.json()); logMsg(d.msg || "\u83b7\u53d6\u5b8c\u6210", "#16a34a"); }
    catch(e) { logMsg("\u83b7\u53d6\u5931\u8d25: " + e.message, "#dc2626"); }
  };
  document.getElementById("btn-select-predict").onclick = async () => {
    logMsg("\u6b63\u5728\u8fd0\u884c\u9884\u6d4b\u7ba1\u9053...", "#2563eb");
    try { const d = await fetch("/api/dashboard/action/run_predict").then(r => r.json()); logMsg(d.msg || "\u9884\u6d4b\u5b8c\u6210", "#16a34a"); }
    catch(e) { logMsg("\u9884\u6d4b\u5931\u8d25: " + e.message, "#dc2626"); }
  };
  lucide.createIcons();
}

// ==================== 2. MATCHES ====================
function filterMatches() {
  const q = document.getElementById("match-search").value.toLowerCase();
  let filtered = allMatchesFlat;
  if (q) filtered = filtered.filter(m => (m.match_id && m.match_id.toLowerCase().includes(q)) || (m.home && m.home.includes(q)) || (m.away && m.away.includes(q)));
  if (currentMatchFilter === "done") filtered = filtered.filter(m => m.actual_score);
  else if (currentMatchFilter === "pred") filtered = filtered.filter(m => m.direction && !m.actual_score);
  else if (currentMatchFilter === "wait") filtered = filtered.filter(m => !m.direction);

  const groups = {};
  filtered.forEach(m => {
    const wd = parseWeekday(m.match_id);
    const key = wd || "other";
    if (!groups[key]) groups[key] = [];
    groups[key].push(m);
  });
  const g = [];
  WEEKDAYS.forEach(wd => { if (groups[wd]) g.push({ sale_date: wd, matches: groups[wd] }); });
  if (groups["other"]) g.push({ sale_date: "\u65e9\u671f", matches: groups["other"] });
  renderMatchGroups(g);
}

function renderMatchGroups(groups) {
  const container = document.getElementById("match-groups");
  let html = "";
  groups.forEach((g, gi) => {
    html += '<div class="match-group"><div class="group-header" data-gi="' + gi + '"><i data-lucide="chevron-right" class="arrow" width="16" height="16"></i>' + g.sale_date + '<span class="count">' + g.matches.length + ' \u573a</span></div><div class="group-body"><table><thead><tr><th>\u7f16\u53f7</th><th>\u4e3b\u961f</th><th>\u5ba2\u961f</th><th>\u65f6\u95f4</th><th>\u4e8b\u4ef6</th><th>\u65b9\u5411</th><th>\u8bc4\u7ea7</th><th>\u8d34\u5408\u5ea6</th><th>\u8d5b\u679c</th></tr></thead><tbody>';
    g.matches.forEach(m => {
      const timeStr = m.match_time ? m.match_time.substring(5, 16) : "\u2014";
      html += '<tr class="' + rowClass(m) + '"><td>' + fmt(m.match_id) + '</td><td>' + fmt(m.home) + '</td><td>' + fmt(m.away) + '</td><td>' + timeStr + '</td><td>' + fmt(m.event) + '</td><td>' + dirBadgeHTML(m.rating, m.direction) + '</td><td>' + fmt(m.rating) + '</td><td>' + fmt1(m.fit_score, "\u2014") + '</td><td>' + fmt(m.actual_score, "\u2014") + '</td></tr>';
    });
    html += '</tbody></table></div></div>';
  });
  container.innerHTML = html || '<div class="empty">\u65e0\u5339\u914d\u6570\u636e</div>';
  container.querySelectorAll(".group-header").forEach(hdr => {
    hdr.addEventListener("click", () => {
      const body = hdr.nextElementSibling;
      const isOpen = body.classList.contains("open");
      container.querySelectorAll(".group-body.open").forEach(b => b.classList.remove("open"));
      container.querySelectorAll(".group-header.open").forEach(b => b.classList.remove("open"));
      if (!isOpen) { body.classList.add("open"); hdr.classList.add("open"); }
    });
  });
  lucide.createIcons();
}

async function loadMatches() {
  const r = await fetch("/api/dashboard/matches_grouped").then(d => d.json());
  allMatchesFlat = [];
  for (const g of (r.groups || [])) {
    for (const m of g.matches) { allMatchesFlat.push(m); }
  }
  filterMatches();
}

// Pill click handler for match toolbar
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("#match-toolbar .pill").forEach(pill => {
    pill.addEventListener("click", function() {
      document.querySelectorAll("#match-toolbar .pill").forEach(p => p.classList.remove("on"));
      this.classList.add("on");
    });
  });
});

// ==================== 3. PREDICTION ====================
async function loadPrediction() {
  const r = await fetch("/api/dashboard/matches_grouped").then(d => d.json());
  let html = "";
  for (const g of (r.groups || [])) {
    for (const m of g.matches) {
      if (!m.direction) continue;
      html += '<div class="pred-card"><div class="pc-header"><div class="pc-teams">' + fmt(m.home) + ' vs ' + fmt(m.away) + '</div>' + dirBadgeHTML(m.rating, m.direction) + '</div>';
      html += '<div class="pc-info"><span>' + fmt(m.match_id) + '</span><span>\u8d34\u5408: ' + fmt1(m.fit_score, "-") + '</span></div>';
      if (m.actual_score) html += '<div class="pc-score">\u8d5b\u679c: ' + m.actual_score + '</div>';
      html += '</div>';
    }
  }
  document.getElementById("pred-cards").innerHTML = html || '<div class="empty">\u6682\u65e0\u9884\u6d4b\u6570\u636e</div>';
  lucide.createIcons();
}

// ==================== 4. PLANS ====================
function _planTag(l) {
  var m = {"\u65b9\u5411":"dir","\u603b\u8fdb\u7403":"tg","\u534a\u5168\u573a":"hf","\u6bd4\u5206":"cs"};
  var baseType = l.type.replace("\u6253\u5305","");
  if(l.packed) return '<span class="plan-tag pk">'+l.type+'</span>';
  return '<span class="plan-tag '+(m[baseType]||"")+'">'+l.type+'</span>';
}
function _planOptStr(l) {
  var s = l.option;
  if(l.packed && l.sub_options) s += ' <span style="color:#9ca3af;font-size:9px">(' + l.sub_options.join("/") + ')</span>';
  return s;
}
function _planReason(c) {
  var p = [];
  p.push(c.l1.match+" \u6a21\u578b\u6982\u7387"+(c.l1.mp*100).toFixed(0)+"%");
  p.push(c.l2.match+" \u6a21\u578b\u6982\u7387"+(c.l2.mp*100).toFixed(0)+"%");
  if(c.l1.fit>=6) p.push(c.l1.match+"\u8d34\u5408\u5ea6"+c.l1.fit);
  if(c.l2.fit>=6) p.push(c.l2.match+"\u8d34\u5408\u5ea6"+c.l2.fit);
  if(c.l1.rating==="A"||c.l2.rating==="A") p.push("\u542b\u6709A\u7ea7\u8bc4\u7ea7");
  p.push("\u4e24\u573a\u6765\u81ea\u4e0d\u540c\u6bd4\u8d5b\uff0c\u98ce\u9669\u5206\u6563");
  p.push("\u4e58\u79ef\u8d54\u7387"+c.odds+"\uff0c\u843d\u5728\u76ee\u6807\u533a\u95f4");
  return "\u4e3a\u4ec0\u4e48\u662f\u5b83\uff1f"+p.join("\u3002")+"\u3002";
}
function _renderPlanCombos(list, cls) {
  if(!list||list.length===0) return '<div class="empty">\u6682\u65e0\u7b26\u5408\u6761\u4ef6\u65b9\u6848</div>';
  var h = '<table class="plan-table"><thead><tr><th>#</th><th>\u7ec4\u5408\u65b9\u6848</th><th>\u8d54\u7387</th><th>\u7efc\u5408\u8bc4\u5206</th></tr></thead><tbody>';
  for(var i=0;i<list.length;i++){
    var c = list[i];
    h += '<tr><td class="td-rank'+(i===0?' top1':'')+'">'+(i+1)+'</td>';
    h += '<td class="td-legs"><div class="lr">'+_planTag(c.l1)+' <span>'+c.l1.option+'</span> <span style="color:#9ca3af">@'+c.l1.odds+'</span> <span style="color:#9ca3af;font-size:11px">'+c.l1.match+'</span> <span class="leg-x">\u00d7</span> '+_planTag(c.l2)+' <span>'+c.l2.option+'</span> <span style="color:#9ca3af">@'+c.l2.odds+'</span> <span style="color:#9ca3af;font-size:11px">'+c.l2.match+'</span></div></td>';
    h += '<td class="td-odds '+cls+'">'+c.odds+'</td>';
    h += '<td class="td-score'+(c.score>0.3?' high':'')+'">'+c.score+'</td></tr>';
  }
  h += '</tbody></table>';
  return h;
}
function _planDataTyp(l) {
  if(l.packed) return "\u6253\u5305";
  return l.type;
}

async function loadPlans() {
  var d = await fetch("/api/dashboard/plan").then(r => r.json());
  if (!d || !d.matches) {
    document.getElementById("plan-content").innerHTML = '<div class="empty">\u6682\u65e0\u8ba1\u5212\u5355\u6570\u636e\uff0c\u8bf7\u5148\u8fd0\u884c python gen_plan.py</div>';
    return;
  }

  var h = "";

  // Stats
  h += '<div class="plan-cols"><div class="plan-col-left"><div class="plan-stats">';
  h += '<div class="plan-stat-card"><span class="sc-num gr">'+d.total_matches+'</span>\u573a\u6bd4\u8d5b</div>';
  h += '<div class="plan-stat-card"><span class="sc-num cy">'+d.total_legs+'</span>\u6761\u817f</div>';
  h += '<div class="plan-stat-card"><span class="sc-num">'+(d.plan_2_count||0)+'</span>\u4e2a2.0\u65b9\u6848</div>';
  h += '<div class="plan-stat-card"><span class="sc-num go">'+(d.plan_3_count||0)+'</span>\u4e2a3.0\u65b9\u6848</div>';
  h += '</div>';

  // Top pick
  if(d.top){
    var tp = d.top;
    h += '<div class="plan-top-pick">';
    h += '<div class="plan-tp-badge">\u2b50 \u672c\u671f\u6700\u63a8\u8350</div>';
    h += '<div class="plan-tp-title">'+tp.l1.match+' \u00d7 '+tp.l2.match+'</div>';
    h += '<div class="plan-tp-sub">\u7efc\u5408\u8bc4\u5206\u6700\u9ad8\u7684\u7a33\u5065\u4e32\u65b9\u6848</div>';
    h += '<div class="plan-tp-legs">';
    h += '<div class="plan-tp-leg"><div class="tpl-match">'+tp.l1.match+'</div><div class="tpl-detail">'+_planTag(tp.l1)+' <span class="hl">'+tp.l1.option+'</span> @<span class="hl2">'+tp.l1.odds+'</span><br>\u6982\u7387 '+(tp.l1.mp*100).toFixed(1)+'% \u00b7 \u8bc4\u5206 '+tp.l1.score+'<br>\u8d34\u5408\u5ea6 '+tp.l1.fit+' \u00b7 '+tp.l1.rating+'</div></div>';
    h += '<div class="plan-tp-leg"><div class="tpl-match">'+tp.l2.match+'</div><div class="tpl-detail">'+_planTag(tp.l2)+' <span class="hl">'+tp.l2.option+'</span> @<span class="hl2">'+tp.l2.odds+'</span><br>\u6982\u7387 '+(tp.l2.mp*100).toFixed(1)+'% \u00b7 \u8bc4\u5206 '+tp.l2.score+'<br>\u8d34\u5408\u5ea6 '+tp.l2.fit+' \u00b7 '+tp.l2.rating+'</div></div>';
    h += '</div>';
    h += '<div class="plan-tp-total"><span class="tpt-odds">\u4e58\u79ef\u8d54\u7387 '+tp.odds+'</span><span class="tpt-score">\u7efc\u5408\u8bc4\u5206 <b style="color:#d97706">'+tp.score+'</b></span></div>';
    h += '<div class="tp-reason">'+_planReason(tp)+'</div></div>';
  }

  // Tabs for 2.0 / 3.0
  h += '</div><div class="plan-col-right"><div class="plan-tabs">';
  h += '<button class="plan-tab active" onclick="planSwitchTab(\'p2\')">2.0\u8ba1\u5212 <span style="font-weight:400;color:#9ca3af">(2.0~3.0)</span></button>';
  h += '<button class="plan-tab" onclick="planSwitchTab(\'p3\')">3.0\u8ba1\u5212 <span style="font-weight:400;color:#9ca3af">(3.0~4.0)</span></button>';
  h += '</div>';
  h += '<div class="plan-tab-content show" id="plan-p2">'+_renderPlanCombos(d.plan_2||[],"")+'</div>';
  h += '<div class="plan-tab-content" id="plan-p3">'+_renderPlanCombos(d.plan_3||[],"")+'</div>';

  h += '</div></div>'; // close cols
  // Legs toggle
  if(d.legs && d.legs.length > 0){
    h += '<div class="legs-toggle" onclick="planToggleLegs()" id="plan-lt"><span class="lt-arrow">\u25b6</span> \u817f\u6c60 \u2014 '+d.legs.length+' \u6761\u5907\u9009\u817f <span style="color:#9ca3af;font-weight:400;margin-left:4px">\u70b9\u51fb\u5c55\u5f00</span></div>';
    h += '<div class="legs-body" id="plan-lb">';
    h += '<div class="legs-filter">';
    var fltTypes = [{k:"all",l:"\u5168\u90e8"},{k:"\u65b9\u5411",l:"\u65b9\u5411"},{k:"\u603b\u8fdb\u7403",l:"\u603b\u8fdb\u7403"},{k:"\u534a\u5168\u573a",l:"\u534a\u5168\u573a"},{k:"\u6bd4\u5206",l:"\u6bd4\u5206"},{k:"\u6253\u5305",l:"\u6253\u5305\u817f"}];
    for(var fi=0;fi<fltTypes.length;fi++){
      h += '<button class="lf-btn'+(fi===0?' active':'')+'" onclick="planFilterLegs(\''+fltTypes[fi].k+'\',this)">'+fltTypes[fi].l+'</button>';
    }
    h += '</div>';
    h += '<table class="legs-table" id="plan-ltbl"><thead><tr><th>#</th><th>\u6bd4\u8d5b</th><th>\u7c7b\u578b</th><th>\u9009\u9879</th><th>\u8d54\u7387</th><th>\u6982\u7387</th><th>\u8bc4\u5206</th><th>\u8d34\u5408</th><th>\u8bc4\u7ea7</th></tr></thead><tbody>';
    for(var i=0;i<d.legs.length;i++){
      var l = d.legs[i];
      var sc = l.score>0.1?"high":(l.score>0.03?"mid":"low");
      h += '<tr class="plan-leg-row" data-typ="'+_planDataTyp(l)+'"><td class="lt-rank">'+(i+1)+'</td>';
      h += '<td class="lt-match">'+l.match+'</td>';
      h += '<td>'+_planTag(l)+'</td><td>'+_planOptStr(l)+'</td>';
      h += '<td class="lt-odds">'+l.odds+'</td>';
      h += '<td>'+(l.mp*100).toFixed(1)+'%</td>';
      h += '<td class="lt-score '+sc+'">'+l.score+'</td>';
      h += '<td>'+l.fit+'</td><td>'+l.rating+'</td></tr>';
    }
    h += '</tbody></table></div>';
  }

  // Logic summary
  h += '<div class="plan-summary"><h3>\u8bc4\u5206\u516c\u5f0f\u4e0e\u7b56\u7565\u8bf4\u660e</h3>';
  h += '<div class="fml">score = model_prob \u00d7 (fit_score / 10)</div>';
  h += '<p>\u8d54\u7387\u6765\u6e90\uff1a\u7ade\u5f69\u7f51 API</p>';
  h += '<p>\u817f\u6c60\u6784\u5efa\uff1a\u6bcf\u573a\u6bd4\u8d5b\u65b9\u5411\u3001\u603b\u8fdb\u7403\u3001\u534a\u5168\u573a\u3001\u6bd4\u5206\u9009\u9879\u6309\u516c\u5f0f\u8ba1\u7b97score</p>';
  h += '<p><b>\u6253\u5305\u817f</b>\uff1a\u5c06\u540c\u4e00\u573a\u6bd4\u8d5b\u3001\u540c\u4e00\u73a9\u6cd5\u7c7b\u578b\u7684 2-3 \u4e2a\u9009\u9879\u6253\u5305\u6210\u4e00\u6761\u865a\u62df\u817f\uff0c\u8d54\u7387 = 1/(1/\u8d54\u73871 + 1/\u8d54\u73872)\uff0c\u6982\u7387 = \u5404\u9009\u9879\u6982\u7387\u4e4b\u548c\uff0cscore = \u5404\u9009\u9879score\u5747\u503c</p>';
  h += '<p>\u652f\u6301\u7684\u6253\u5305\u7c7b\u578b\uff1a\u603b\u8fdb\u7403 2/3\u7403\u3001\u603b\u8fdb\u7403 3/4\u7403\u3001\u534a\u5168\u573a \u4e3b\u4e0d\u8d25(\u80dc\u80dc+\u5e73\u80dc)\u3001\u534a\u5168\u573a \u5ba2\u4e0d\u8d25(\u8d1f\u8d1f+\u5e73\u8d1f)\u3001\u6bd4\u5206 \u4e3b\u5c0f\u80dc(1-0+2-0)\u3001\u6bd4\u5206 \u5ba2\u5c0f\u80dc(0-1+0-2)\u3001\u65b9\u5411\u8ba9\u7403\u76d8 \u8ba9\u80dc/\u5e73\u3001\u65b9\u5411\u8ba9\u7403\u76d8 \u8ba9\u5e73/\u8d1f</p>';
  h += '<p>\u4ece\u817f\u6c60\u53d6\u4e24\u6761\u817f\uff0c\u5fc5\u987b\u6765\u81ea\u4e0d\u540c\u6bd4\u8d5b\uff0c\u6309\u4e58\u79ef\u8d54\u7387\u5206\u4e3a2.0\u8ba1\u5212(2.0~3.0)\u548c3.0\u8ba1\u5212(3.0~4.0)</p>';
  h += '<div style="margin-top:10px;padding:8px 12px;background:rgba(220,38,38,.04);border-radius:6px;border:1px solid rgba(220,38,38,.1);font-size:11px">\u26a0\ufe0f \u4ee5\u4e0a\u5185\u5bb9\u5747\u7531\u6570\u636e\u5206\u6790\u7cfb\u7edf\u81ea\u52a8\u751f\u6210\uff0c\u4ec5\u4f9b\u53c2\u8003\uff0c\u4e0d\u6784\u6210\u6295\u6ce8\u5efa\u8bae\u3002</div></div>';

  document.getElementById("plan-content").innerHTML = h;
  lucide.createIcons();
}

// Plan panel helper functions (global scope)
function planSwitchTab(id) {
  document.querySelectorAll(".plan-tab").forEach(function(t){t.classList.remove("active");});
  document.querySelectorAll(".plan-tab-content").forEach(function(t){t.classList.remove("show");});
  if(id==="p2"){document.querySelectorAll(".plan-tab")[0].classList.add("active");document.getElementById("plan-p2").classList.add("show");}
  else{document.querySelectorAll(".plan-tab")[1].classList.add("active");document.getElementById("plan-p3").classList.add("show");}
}
function planToggleLegs() {
  document.getElementById("plan-lb").classList.toggle("open");
  document.getElementById("plan-lt").classList.toggle("open");
}
function planFilterLegs(typ, btn) {
  document.querySelectorAll(".lf-btn").forEach(function(b){b.classList.remove("active");});
  btn.classList.add("active");
  document.querySelectorAll(".plan-leg-row").forEach(function(r){
    r.style.display=(typ==="all"||r.getAttribute("data-typ")===typ)?"":"none";
  });
}

// ==================== 5. REVIEW ====================
async function loadReview() {
  const r = await fetch("/api/dashboard/review").then(d => d.json());
  document.getElementById("rv-total").textContent = r.total || 0;
  document.getElementById("rv-hits").textContent = r.hit || 0;
  document.getElementById("rv-hitrate").textContent = (r.hitrate || 0) + "%";
  document.getElementById("rv-ratings").innerHTML = '<div class="rv-num">' + (r.hit || 0) + '/' + (r.total || 0) + '</div><div class="rv-label">\u547d\u4e2d/\u603b\u8ba1</div>';

  let html = "";
  for (const item of (r.review_list || [])) {
    html += '<div class="rv-item ' + (item.hit ? "hit" : "miss") + '"><span class="rv-teams">' + item.match_id + ' ' + fmt(item.home) + ' vs ' + fmt(item.away) + '</span><span>' + fmt(item.actual_score) + '</span>' + dirBadgeHTML(item.rating, item.direction) + '<span>' + (item.hit ? "\u2705" : "\u274c") + '</span></div>';
  }
  document.getElementById("rv-list").innerHTML = html || '<div class="empty">\u6682\u65e0\u590d\u76d8\u6570\u636e</div>';
  lucide.createIcons();
}

// ==================== 6. SYSTEM ====================
async function loadSystem() {
  if (!overviewData) overviewData = await fetch("/api/dashboard/overview").then(d => d.json());
  const r = await fetch("/api/dashboard/analysis").then(d => d.json());
  document.getElementById("sys-status").innerHTML =
    '<div><strong>\u6570\u636e\u5e93</strong>: ' + (overviewData.stats ? overviewData.stats.total + ' \u6761\u8bb0\u5f55' : '-') + '</div>' +
    '<div><strong>APP \u6570\u636e</strong>: ' + (r.total_ratings || 0) + ' \u6761\u8bc4\u5206, ' + (r.completed || 0) + ' \u5df2\u5b8c\u6210, ' + (r.predicted || 0) + ' \u9884\u6d4b\u4e2d</div>' +
    '<div><strong>\u9500\u552e\u65e5\u671f</strong>: ' + (r.al_keys || []).join(" \u2192 ") + '</div>' +
    '<div style="margin-top:8px;color:#6b7280;font-size:12px">V3.3.3-Core \u00b7 ' + new Date().toLocaleDateString("zh-CN") + '</div>';
  lucide.createIcons();
}

// ==================== INIT ====================
document.getElementById("loadingOverlay").style.display = "none";
overview();
lucide.createIcons();
