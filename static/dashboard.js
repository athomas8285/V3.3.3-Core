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
async function loadPlans() {
  if (!overviewData) overviewData = await fetch("/api/dashboard/overview").then(d => d.json());
  document.getElementById("plan-content").innerHTML =
    '<div class="stat-card"><div class="num">' + (overviewData.plan_info ? overviewData.plan_info.total_matches || "-" : "-") + '</div><div class="label">\u8ba1\u5212\u5355\u6bd4\u8d5b</div></div>' +
    '<div class="stat-card"><div class="num">' + (overviewData.plan_info ? overviewData.plan_info.plan_count || "-" : "-") + '</div><div class="label">\u65b9\u6848\u6570</div></div>';
  lucide.createIcons();
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
