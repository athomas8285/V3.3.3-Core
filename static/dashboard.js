// ==================== GLOBALS ====================
const WEEKDAYS = ["周一","周二","周三","周四","周五","周六","周日"];
let overviewData = null;
let matchGroups = null;
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
function dirBadgeHTML(rating, direction) {
  const cls = rating || "";
  return '<span class="dir-badge ' + cls + '">' + fmt(direction, "\u2014") + '</span>';
}
function parseWeekday(mid) {
  for (const wd of WEEKDAYS) {
    if (mid && mid.startsWith(wd)) return wd;
  }
  return null;
}

// ==================== SIDEBAR NAV ====================
document.querySelectorAll(".nav-item").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".nav-item").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    const panelId = "panel-" + btn.dataset.panel;
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    document.getElementById(panelId).classList.add("active");
    loadPanel(btn.dataset.panel);
  });
});

document.getElementById("collapse-btn").addEventListener("click", () => {
  const sb = document.getElementById("sidebar");
  sb.classList.toggle("collapsed");
  const icon = document.querySelector("#collapse-btn i");
  if (sb.classList.contains("collapsed")) {
    icon.setAttribute("data-lucide", "panel-left-open");
  } else {
    icon.setAttribute("data-lucide", "panel-left-close");
  }
  lucide.createIcons();
  // Console buttons
  const clog = document.getElementById("console-log");
  function logMsg(msg, color) {
    clog.style.display = "block";
    const now = new Date().toLocaleTimeString("zh-CN");
    clog.innerHTML += '<div style="color:' + (color || "#6b7280") + '">[' + now + '] ' + msg + '</div>';
    clog.scrollTop = clog.scrollHeight;
  }
  document.getElementById("btn-fetch-results").addEventListener("click", async () => {
    logMsg("正在查询赛果...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/fetch_results");
      const d = await r.json();
      logMsg(d.msg || "查询完成", "#16a34a");
    } catch(e) {
      logMsg("查询失败: " + e.message, "#dc2626");
    }
  });
  document.getElementById("btn-manual-entry").addEventListener("click", () => {
    logMsg("请在比赛模块中手动编辑比分和半全场", "#d97706");
    document.querySelector('.nav-item[data-panel="matches"]').click();
  });
  document.getElementById("btn-fetch-jczq").addEventListener("click", async () => {
    logMsg("正在从竞彩网获取比赛...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/fetch_jczq");
      const d = await r.json();
      logMsg(d.msg || "获取完成", "#16a34a");
    } catch(e) {
      logMsg("获取失败: " + e.message, "#dc2626");
    }
  });
  document.getElementById("btn-select-predict").addEventListener("click", async () => {
    logMsg("正在运行预测管道...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/run_predict");
      const d = await r.json();
      logMsg(d.msg || "预测完成", "#16a34a");
    } catch(e) {
      logMsg("预测失败: " + e.message, "#dc2626");
    }
  });
});

function updateSidebarTime() {
  const now = new Date();
  document.getElementById("sidebar-time").textContent =
    now.toLocaleString("zh-CN", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}
setInterval(updateSidebarTime, 1000);
updateSidebarTime();

// ==================== PANEL LOADING ====================
const panelLoaders = { overview, console, matches, prediction, plans, review, system };
async function loadPanel(name) {
  if (panelLoaded[name]) return;
  panelLoaded[name] = true;
  await panelLoaders[name]();
}

// ==================== CHART ====================
function drawTrendChart(canvasId, trend) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || !trend.length) {
    if (canvas) {
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    return;
  }
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

  // Axes
  ctx.strokeStyle = "#e5e7eb";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pad.left, pad.top);
  ctx.lineTo(pad.left, pad.top + ph);
  ctx.lineTo(pad.left + pw, pad.top + ph);
  ctx.stroke();

  // Y ticks
  ctx.fillStyle = "#9ca3af";
  ctx.font = "10px -apple-system,BlinkMacSystemFont,sans-serif";
  ctx.textAlign = "right";
  for (let i = 0; i <= 4; i++) {
    const y = pad.top + ph * (1 - i / 4);
    ctx.fillText(i * 25 + "%", pad.left - 6, y + 3);
    ctx.strokeStyle = "#f3f4f6";
    ctx.beginPath();
    ctx.moveTo(pad.left + 1, y);
    ctx.lineTo(pad.left + pw, y);
    ctx.stroke();
  }

  // Line
  ctx.strokeStyle = "#2563eb";
  ctx.lineWidth = 2;
  ctx.beginPath();
  trend.forEach((t, i) => {
    const x = pad.left + i * stepX;
    const y = pad.top + ph * (1 - t.rate / 100);
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  });
  ctx.stroke();

  // Dots & labels
  ctx.fillStyle = "#2563eb";
  ctx.textAlign = "center";
  ctx.font = "10px -apple-system,BlinkMacSystemFont,sans-serif";
  trend.forEach((t, i) => {
    const x = pad.left + i * stepX;
    const y = pad.top + ph * (1 - t.rate / 100);
    ctx.beginPath();
    ctx.arc(x, y, 3, 0, Math.PI * 2);
    ctx.fill();
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

// ==================== 2. MATCHES ====================
function filterMatches() {
  const q = document.getElementById("match-search").value.toLowerCase();
  let filtered = allMatchesFlat;
  if (q) {
    filtered = filtered.filter(m =>
      (m.match_id && m.match_id.toLowerCase().includes(q)) ||
      (m.home && m.home.includes(q)) ||
      (m.away && m.away.includes(q))
    );
  }
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
    html += '<div class="match-group">' +
      '<div class="group-header" data-gi="' + gi + '">' +
      '<i data-lucide="chevron-right" class="arrow" width="16" height="16"></i>' +
      g.sale_date +
      '<span class="count">' + g.matches.length + ' \u573a</span>' +
      '</div>' +
      '<div class="group-body">' +
      '<table><thead><tr>' +
      '<th>\u7f16\u53f7</th><th>\u4e3b\u961f</th><th>\u5ba2\u961f</th><th>\u65f6\u95f4</th><th>\u4e8b\u4ef6</th><th>\u65b9\u5411</th><th>\u8bc4\u7ea7</th><th>\u8d34\u5408\u5ea6</th><th>\u8d5b\u679c</th>' +
      '</tr></thead><tbody>';
    g.matches.forEach(m => {
      const timeStr = m.match_time ? m.match_time.substring(5, 16) : "\u2014";
      html += '<tr class="' + rowClass(m) + '">' +
        '<td>' + fmt(m.match_id) + '</td>' +
        '<td>' + fmt(m.home) + '</td>' +
        '<td>' + fmt(m.away) + '</td>' +
        '<td>' + timeStr + '</td>' +
        '<td>' + fmt(m.event) + '</td>' +
        '<td style="white-space:nowrap">' + dirBadgeHTML(m.rating, m.direction) + '</td>' +
        '<td>' + fmt(m.rating) + '</td>' +
        '<td>' + fmt1(m.fit_score, "\u2014") + '</td>' +
        '<td>' + fmt(m.actual_score, "\u2014") + '</td>' +
        '</tr>';
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
      if (!isOpen) {
        body.classList.add("open");
        hdr.classList.add("open");
      }
    });
  });

  lucide.createIcons();
}
async function prediction() {
  if (!overviewData) {
    overviewData = await fetch("/api/dashboard/overview").then(d => d.json());
  }
  const todayMatches = overviewData.today_matches || [];
  const predCards = document.getElementById("pred-cards");
  let html = "";
  todayMatches.forEach(m => {
    const hasPred = m.direction && m.direction !== "";
    const timeStr = (m.match_time || "").substring(5, 16);
    html += '<div class="pred-card" data-mid="' + m.match_id + '">' +
      '<div class="teams">' + fmt(m.home) + ' vs ' + fmt(m.away) + '</div>' +
      '<div class="meta">' + timeStr + '</div>' +
      '<div style="margin-top:6px">' +
      (hasPred ? dirBadgeHTML(m.rating, m.direction) + ' <span style="font-size:12px;color:#9ca3af">\u8d34\u5408 ' + fmt1(m.fit_score, "\u2014") + '</span>' : '<span style="font-size:12px;color:#9ca3af">\u5f85\u9884\u6d4b</span>') +
      '</div></div>';
  });
  predCards.innerHTML = html || '<div class="empty">\u4eca\u65e5\u65e0\u6bd4\u8d5b</div>';

  if (todayMatches.length > 0) {
    selectPredMatch(todayMatches[0].match_id);
  }

  predCards.querySelectorAll(".pred-card").forEach(card => {
    card.addEventListener("click", () => selectPredMatch(card.dataset.mid));
  });

  lucide.createIcons();
  // Console buttons
  const clog = document.getElementById("console-log");
  function logMsg(msg, color) {
    clog.style.display = "block";
    const now = new Date().toLocaleTimeString("zh-CN");
    clog.innerHTML += '<div style="color:' + (color || "#6b7280") + '">[' + now + '] ' + msg + '</div>';
    clog.scrollTop = clog.scrollHeight;
  }
  document.getElementById("btn-fetch-results").addEventListener("click", async () => {
    logMsg("正在查询赛果...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/fetch_results");
      const d = await r.json();
      logMsg(d.msg || "查询完成", "#16a34a");
    } catch(e) {
      logMsg("查询失败: " + e.message, "#dc2626");
    }
  });
  document.getElementById("btn-manual-entry").addEventListener("click", () => {
    logMsg("请在比赛模块中手动编辑比分和半全场", "#d97706");
    document.querySelector('.nav-item[data-panel="matches"]').click();
  });
  document.getElementById("btn-fetch-jczq").addEventListener("click", async () => {
    logMsg("正在从竞彩网获取比赛...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/fetch_jczq");
      const d = await r.json();
      logMsg(d.msg || "获取完成", "#16a34a");
    } catch(e) {
      logMsg("获取失败: " + e.message, "#dc2626");
    }
  });
  document.getElementById("btn-select-predict").addEventListener("click", async () => {
    logMsg("正在运行预测管道...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/run_predict");
      const d = await r.json();
      logMsg(d.msg || "预测完成", "#16a34a");
    } catch(e) {
      logMsg("预测失败: " + e.message, "#dc2626");
    }
  });
}

// ==================== 4. PLANS ====================
async function plans() {
  const container = document.getElementById("plan-content");
  let plan = null;
  try {
    const r = await fetch("/api/dashboard/overview");
    const ov = await r.json();
    if (ov.plan_info && ov.plan_info.date) {
      // Fetch actual plan data
      const pr = await fetch("/data/plan_data.json");
      if (pr.ok) plan = await pr.json();
    }
  } catch(e) {}

  if (!plan || (!plan.plan_2 || !plan.plan_2.length) && (!plan.plan_3 || !plan.plan_3.length)) {
    container.innerHTML = '<div class="empty">\u5c1a\u672a\u751f\u6210\u4eca\u65e5\u8ba1\u5212\u5355<br><span style="font-size:12px;color:#484f58">\u8bf7\u8fd0\u884c gen_plan.py \u751f\u6210</span></div>';
    return;
  }

  let html = '<div style="font-size:13px;color:#9ca3af;margin-bottom:12px">\u65e5\u671f: ' + fmt(plan.date) + ' | \u6bd4\u8d5b: ' + fmt(plan.total_matches) + ' \u573a</div>';
  const allPlans = (plan.plan_2 || []).concat(plan.plan_3 || []);
  html += '<div class="plan-list">';
  allPlans.forEach((p, i) => {
    const pid = p.plan_id || ("P" + (i + 1));
    const score = p.total_score || p.score || "\u2014";
    const legs = p.legs || [];
    html += '<div class="plan-item">' +
      '<div class="plan-head"><span class="plan-id">' + pid + '</span><span class="plan-score">\u8bc4\u5206: ' + fmt(score) + '</span></div>' +
      '<div class="plan-matches">';
    legs.forEach(leg => {
      html += '<span class="plan-match">' + fmt(leg.match_id || leg.id) + ' ' + fmt(leg.home) + ' vs ' + fmt(leg.away) + '</span>';
    });
    html += '</div></div>';
  });
  html += '</div>';
  container.innerHTML = html;
}

// ==================== 5. REVIEW ====================
async function review() {
  const r = await fetch("/api/dashboard/review").then(d => d.json());

  document.getElementById("rv-hitrate").textContent = r.cumulative.rate + "%";
  document.getElementById("rv-total").textContent = r.cumulative.total;
  document.getElementById("rv-hits").textContent = r.cumulative.hits;

  let ratingHTML = "";
  (r.rating_stats || []).forEach(rs => {
    ratingHTML += '<div class="stat-card" style="flex:1;min-width:80px"><div class="num ' + (rs.rate >= 50 ? "green" : "red") + '">' + rs.rate + '%</div><div class="label">' + rs.rating + ' \u7ea7 (' + rs.hits + '/' + rs.total + ')</div></div>';
  });
  document.getElementById("rv-ratings").innerHTML = ratingHTML || '<span style="color:#9ca3af">\u6682\u65e0\u6570\u636e</span>';

  drawTrendChart("rv-chart", r.trend || []);

  let listHTML = "";
  (r.completed || []).forEach(m => {
    const isHit = m.hit === 1;
    listHTML += '<div class="review-row">' +
      '<span class="teams">' + fmt(m.match_id) + ' ' + fmt(m.home) + ' vs ' + fmt(m.away) + '</span>' +
      '<span class="pred">' + fmt(m.direction) + ' ' + (m.rating || "") + '</span>' +
      '<span class="score">' + fmt(m.actual_score, "\u2014") + '</span>' +
      '<span class="hit-icon ' + (isHit ? "hit-true" : "hit-false") + '">' + (isHit ? "\u2713" : "\u2717") + '</span>' +
      '</div>';
    if (!isHit && m.diagnosis) {
      listHTML += '<div style="font-size:12px;color:#9ca3af;padding:0 0 8px 16px">\u8bca\u65ad: ' + m.diagnosis + '</div>';
    }
  });
  document.getElementById("rv-list").innerHTML = listHTML || '<div class="empty">\u6682\u65e0\u590d\u76d8\u6570\u636e</div>';
}

// ==================== 6. SYSTEM ====================
async function system() {
  if (!overviewData) {
    overviewData = await fetch("/api/dashboard/overview").then(d => d.json());
  }
  const s = overviewData.stats || {};
  document.getElementById("sys-status").innerHTML =
    '<div class="sys-card"><div class="sys-val">' + s.total + '</div><div class="sys-lbl">DB \u8bb0\u5f55\u6570</div></div>' +
    '<div class="sys-card"><div class="sys-val">' + new Date().toLocaleDateString("zh-CN") + '</div><div class="sys-lbl">\u6700\u540e\u66f4\u65b0</div></div>' +
    '<div class="sys-card"><div class="sys-val" style="color:#16a34a">\u2713</div><div class="sys-lbl">\u7ade\u5f69\u7f51 API</div></div>' +
    '<div class="sys-card"><div class="sys-val" style="color:#d29922">\u25cb</div><div class="sys-lbl">APP \u6570\u636e\u540c\u6b65</div></div>';
  lucide.createIcons();
  // Console buttons
  const clog = document.getElementById("console-log");
  function logMsg(msg, color) {
    clog.style.display = "block";
    const now = new Date().toLocaleTimeString("zh-CN");
    clog.innerHTML += '<div style="color:' + (color || "#6b7280") + '">[' + now + '] ' + msg + '</div>';
    clog.scrollTop = clog.scrollHeight;
  }
  document.getElementById("btn-fetch-results").addEventListener("click", async () => {
    logMsg("正在查询赛果...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/fetch_results");
      const d = await r.json();
      logMsg(d.msg || "查询完成", "#16a34a");
    } catch(e) {
      logMsg("查询失败: " + e.message, "#dc2626");
    }
  });
  document.getElementById("btn-manual-entry").addEventListener("click", () => {
    logMsg("请在比赛模块中手动编辑比分和半全场", "#d97706");
    document.querySelector('.nav-item[data-panel="matches"]').click();
  });
  document.getElementById("btn-fetch-jczq").addEventListener("click", async () => {
    logMsg("正在从竞彩网获取比赛...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/fetch_jczq");
      const d = await r.json();
      logMsg(d.msg || "获取完成", "#16a34a");
    } catch(e) {
      logMsg("获取失败: " + e.message, "#dc2626");
    }
  });
  document.getElementById("btn-select-predict").addEventListener("click", async () => {
    logMsg("正在运行预测管道...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/run_predict");
      const d = await r.json();
      logMsg(d.msg || "预测完成", "#16a34a");
    } catch(e) {
      logMsg("预测失败: " + e.message, "#dc2626");
    }
  });
}

// ==================== INIT ====================
window.onload = async () => {
  await overview();
  lucide.createIcons();
  // Console buttons
  const clog = document.getElementById("console-log");
  function logMsg(msg, color) {
    clog.style.display = "block";
    const now = new Date().toLocaleTimeString("zh-CN");
    clog.innerHTML += '<div style="color:' + (color || "#6b7280") + '">[' + now + '] ' + msg + '</div>';
    clog.scrollTop = clog.scrollHeight;
  }
  document.getElementById("btn-fetch-results").addEventListener("click", async () => {
    logMsg("正在查询赛果...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/fetch_results");
      const d = await r.json();
      logMsg(d.msg || "查询完成", "#16a34a");
    } catch(e) {
      logMsg("查询失败: " + e.message, "#dc2626");
    }
  });
  document.getElementById("btn-manual-entry").addEventListener("click", () => {
    logMsg("请在比赛模块中手动编辑比分和半全场", "#d97706");
    document.querySelector('.nav-item[data-panel="matches"]').click();
  });
  document.getElementById("btn-fetch-jczq").addEventListener("click", async () => {
    logMsg("正在从竞彩网获取比赛...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/fetch_jczq");
      const d = await r.json();
      logMsg(d.msg || "获取完成", "#16a34a");
    } catch(e) {
      logMsg("获取失败: " + e.message, "#dc2626");
    }
  });
  document.getElementById("btn-select-predict").addEventListener("click", async () => {
    logMsg("正在运行预测管道...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/run_predict");
      const d = await r.json();
      logMsg(d.msg || "预测完成", "#16a34a");
    } catch(e) {
      logMsg("预测失败: " + e.message, "#dc2626");
    }
  });
};// ==================== CONSOLE ====================
async function console() {
  const r = await fetch("/api/dashboard/overview").then(d => d.json());
  const s = r.stats;

  document.getElementById("console-tasks").innerHTML =
    '<div class="task-card" data-nav="matches"><div class="task-num red">' + r.missing_results + '</div><div class="task-label">需补赛果</div></div>' +
    '<div class="task-card" data-nav="prediction"><div class="task-num yellow">' + (s.total - s.predicted) + '</div><div class="task-label">待预测</div></div>' +
    '<div class="task-card" data-nav="review"><div class="task-num green">' + (s.hit + s.miss) + '</div><div class="task-label">可复盘</div></div>' +
    '<div class="task-card" data-nav="plans"><div class="task-num gray">' + (r.plan_info ? r.plan_info.plan_count : "—") + '</div><div class="task-label">计划单</div></div>';

  document.querySelectorAll("#console-tasks .task-card").forEach(card => {
    card.addEventListener("click", () => {
      const panel = card.dataset.nav;
      document.querySelector('.nav-item[data-panel="' + panel + '"]').click();
    });
  });

  const clog = document.getElementById("console-log");
  function logMsg(msg, color) {
    clog.style.display = "block";
    const now = new Date().toLocaleTimeString("zh-CN");
    clog.innerHTML += '<div style="color:' + (color || "#6b7280") + '">[' + now + '] ' + msg + '</div>';
    clog.scrollTop = clog.scrollHeight;
  }
  document.getElementById("btn-fetch-results").onclick = async () => {
    logMsg("正在查询赛果...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/fetch_results");
      const d = await r.json();
      logMsg(d.msg || "查询完成", "#16a34a");
    } catch(e) {
      logMsg("查询失败: " + e.message, "#dc2626");
    }
  };
  document.getElementById("btn-manual-entry").onclick = () => {
    logMsg("请在比赛模块中手动编辑比分和半全场", "#d97706");
    document.querySelector('.nav-item[data-panel="matches"]').click();
  };
  document.getElementById("btn-fetch-jczq").onclick = async () => {
    logMsg("正在从竞彩网获取比赛...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/fetch_jczq");
      const d = await r.json();
      logMsg(d.msg || "获取完成", "#16a34a");
    } catch(e) {
      logMsg("获取失败: " + e.message, "#dc2626");
    }
  };
  document.getElementById("btn-select-predict").onclick = async () => {
    logMsg("正在运行预测管道...", "#2563eb");
    try {
      const r = await fetch("/api/dashboard/action/run_predict");
      const d = await r.json();
      logMsg(d.msg || "预测完成", "#16a34a");
    } catch(e) {
      logMsg("预测失败: " + e.message, "#dc2626");
    }
  };
}


