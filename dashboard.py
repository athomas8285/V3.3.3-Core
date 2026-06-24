import json, os
from datetime import date
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder="templates")
BASE = "D:/V3.3.3-Core"
APP_DATA = "C:/Users/gjj/Documents/Codex/2026-06-14/app-app/outputs/data"

def db_get():
    import sqlite3
    conn = sqlite3.connect(os.path.join(BASE, "framework.db"))
    conn.row_factory = sqlite3.Row
    return conn

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# ==================== Helpers ====================

WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

def parse_weekday(match_id):
    for wd in WEEKDAY_CN:
        if match_id.startswith(wd):
            return wd
    return None

def get_today_cn():
    return WEEKDAY_CN[date.today().weekday()]

# Cross-run result lookup: for a given match_id, find the latest non-null actual_score/hit/diagnosis
# across all runs. Prediction fields (direction, rating, fit_score, lambda, DDI etc.)
# are taken from the latest run (run_id = max).
_RESULT_CACHE = None

def _build_result_cache(db):
    """Build a dict of match_id -> {actual_score, hit, diagnosis} from the latest non-null across all runs."""
    global _RESULT_CACHE
    rows = db.execute(
        "SELECT match_id, actual_score, hit, diagnosis FROM matches WHERE actual_score IS NOT NULL AND actual_score != '' ORDER BY run_id DESC"
    ).fetchall()
    _RESULT_CACHE = {}
    for r in rows:
        if r["match_id"] not in _RESULT_CACHE:
            _RESULT_CACHE[r["match_id"]] = {
                "actual_score": r["actual_score"],
                "hit": r["hit"],
                "diagnosis": r["diagnosis"]
            }

def get_results_for(match_ids):
    """Return list of {match_id, actual_score, hit, diagnosis} for given match_ids."""
    if _RESULT_CACHE is None:
        return []
    return [_RESULT_CACHE.get(mid, {}) for mid in match_ids]

def enrich_row_with_results(row_dict):
    """Add actual_score/hit/diagnosis from cross-run cache to a row from latest run."""
    mid = row_dict.get("match_id", "")
    if _RESULT_CACHE and mid in _RESULT_CACHE:
        r = _RESULT_CACHE[mid]
        if not row_dict.get("actual_score"):
            row_dict["actual_score"] = r["actual_score"]
        if row_dict.get("hit") is None:
            row_dict["hit"] = r["hit"]
        if not row_dict.get("diagnosis"):
            row_dict["diagnosis"] = r["diagnosis"]
    return row_dict

# ==================== Routes ====================

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/dashboard/stats")
def stats():
    db = db_get()
    _build_result_cache(db)
    rid = db.execute("SELECT MAX(run_id) FROM matches").fetchone()[0]
    
    # Counts from latest run
    total = db.execute("SELECT COUNT(*) FROM matches WHERE run_id=?", (rid,)).fetchone()[0]
    predicted = db.execute("SELECT COUNT(*) FROM matches WHERE run_id=? AND direction IS NOT NULL AND direction != ''", (rid,)).fetchone()[0]
    
    # Scored/hit/miss counted from cross-run results (unique match_ids)
    all_rows = db.execute("SELECT match_id FROM matches WHERE run_id=?", (rid,)).fetchall()
    match_ids = [r["match_id"] for r in all_rows]
    
    scored = 0; hit = 0; miss = 0
    for mid in match_ids:
        if mid in _RESULT_CACHE:
            scored += 1
            h = _RESULT_CACHE[mid]["hit"]
            if h == 1: hit += 1
            elif h == 0: miss += 1
    
    need_predict = db.execute("SELECT COUNT(*) FROM matches WHERE run_id=? AND (direction IS NULL OR direction = '')", (rid,)).fetchone()[0]
    recent = db.execute("SELECT match_id, home, away, match_time, event, direction, rating, actual_score, hit, fit_score FROM matches WHERE run_id=? ORDER BY match_id DESC LIMIT 20", (rid,)).fetchall()
    recent_list = [enrich_row_with_results({k: r[k] for k in r.keys()}) for r in recent]
    
    db.close()
    
    analysis = load_json(os.path.join(APP_DATA, "analysis.json"))
    al = list(analysis.get("AL", {}).keys()) if analysis else []
    return jsonify({
        "total": total, "scored": scored, "predicted": predicted,
        "hit": hit, "miss": miss, "today_need_predict": need_predict,
        "al_groups": al, "recent": recent_list
    })

@app.route("/api/dashboard/matches")
def matches():
    db = db_get()
    _build_result_cache(db)
    rid = db.execute("SELECT MAX(run_id) FROM matches").fetchone()[0]
    rows = db.execute(
        "SELECT match_id, home, away, match_time, event, direction, rating, actual_score, hit, fit_score, half_full, jc_sp_home, jc_sp_draw, jc_sp_away, jc_handicap FROM matches WHERE run_id=? ORDER BY match_id",
        (rid,)
    ).fetchall()
    db.close()
    return jsonify([enrich_row_with_results({k: r[k] for k in r.keys()}) for r in rows])

@app.route("/api/dashboard/analysis")
def analysis():
    data = load_json(os.path.join(APP_DATA, "analysis.json"))
    if not data:
        return jsonify({"error": "no analysis.json"})
    ratings = data.get("rating", [])
    return jsonify({
        "total_ratings": len(ratings),
        "completed": len([r for r in ratings if r.get("actual_score")]),
        "predicted": len([r for r in ratings if r.get("direction") and not r.get("actual_score")]),
        "waiting": len([r for r in ratings if not r.get("direction")]),
        "al_keys": list(data.get("AL", {}).keys())
    })

# ==================== New endpoints ====================

@app.route("/api/dashboard/overview")
def overview():
    db = db_get()
    _build_result_cache(db)
    rid = db.execute("SELECT MAX(run_id) FROM matches").fetchone()[0]
    
    total = db.execute("SELECT COUNT(*) FROM matches WHERE run_id=?", (rid,)).fetchone()[0]
    predicted = db.execute("SELECT COUNT(*) FROM matches WHERE run_id=? AND direction IS NOT NULL AND direction != ''", (rid,)).fetchone()[0]
    
    all_rows = db.execute("SELECT match_id FROM matches WHERE run_id=?", (rid,)).fetchall()
    match_ids = [r["match_id"] for r in all_rows]
    
    scored = 0; hit = 0; miss = 0
    for mid in match_ids:
        if mid in _RESULT_CACHE:
            scored += 1
            h = _RESULT_CACHE[mid]["hit"]
            if h == 1: hit += 1
            elif h == 0: miss += 1
    
    hitrate = round(hit / (hit + miss) * 100, 1) if (hit + miss) > 0 else 0
    
    today_wd = get_today_cn()
    all_match_rows = db.execute(
        "SELECT id, match_id, home, away, match_time, event, league, direction, rating, fit_score, actual_score, hit FROM matches WHERE run_id=? ORDER BY match_id",
        (rid,)
    ).fetchall()
    today_matches_raw = [r for r in all_match_rows if r["match_id"].startswith(today_wd)]
    today_matches = [enrich_row_with_results({k: r[k] for k in r.keys()}) for r in today_matches_raw]
    
    missing_results = scored - (hit + miss)  # matches with score but hit not set
    sp_missing = db.execute("SELECT COUNT(*) FROM matches WHERE run_id=? AND sp_missing=1", (rid,)).fetchone()[0]
    
    recent_raw = db.execute(
        "SELECT id, match_id, home, away, match_time, event, direction, rating, fit_score, actual_score, hit FROM matches WHERE run_id=? AND direction IS NOT NULL AND direction != '' ORDER BY id DESC LIMIT 4",
        (rid,)
    ).fetchall()
    recent_predictions = [enrich_row_with_results({k: r[k] for k in r.keys()}) for r in recent_raw]
    
    # Hit trend from cross-run results
    trend_map = {}
    for mid in match_ids:
        if mid in _RESULT_CACHE:
            h = _RESULT_CACHE[mid]["hit"]
            if h is not None:
                wd = parse_weekday(mid)
                key = wd if wd else "other"
                if key not in trend_map:
                    trend_map[key] = {"total": 0, "hit": 0}
                trend_map[key]["total"] += 1
                if h == 1:
                    trend_map[key]["hit"] += 1
    
    trend = []
    for wd in WEEKDAY_CN:
        if wd in trend_map:
            t = trend_map[wd]
            trend.append({"label": wd, "hit": t["hit"], "total": t["total"], "rate": round(t["hit"]/t["total"]*100, 1) if t["total"] else 0})
    if "other" in trend_map:
        t = trend_map["other"]
        trend.append({"label": "\u65e9\u671f", "hit": t["hit"], "total": t["total"], "rate": round(t["hit"]/t["total"]*100, 1) if t["total"] else 0})
    
    plan = load_json(os.path.join(BASE, "data", "plan_data.json"))
    plan_info = None
    if plan:
        p2 = len(plan.get("plan_2", []))
        p3 = len(plan.get("plan_3", []))
        plan_info = {"date": plan.get("date"), "total_matches": plan.get("total_matches"), "plan_count": p2 + p3}
    
    db.close()
    
    return jsonify({
        "stats": {"total": total, "scored": scored, "predicted": predicted, "hit": hit, "miss": miss, "hitrate": hitrate},
        "today_matches": today_matches,
        "missing_results": missing_results,
        "health": {"sp_missing": sp_missing, "total": total},
        "recent_predictions": recent_predictions,
        "hit_trend": trend,
        "plan_info": plan_info
    })

@app.route("/api/dashboard/matches_grouped")
def matches_grouped():
    db = db_get()
    _build_result_cache(db)
    rid = db.execute("SELECT MAX(run_id) FROM matches").fetchone()[0]
    rows = db.execute(
        "SELECT id, match_id, home, away, match_time, event, league, direction, rating, fit_score, actual_score, hit, half_full, jc_sp_home, jc_sp_draw, jc_sp_away, jc_handicap, asian_handicap, ah_home, ah_draw, ah_away FROM matches WHERE run_id=? ORDER BY match_id",
        (rid,)
    ).fetchall()
    db.close()
    
    groups = {}
    for r in rows:
        enriched = enrich_row_with_results({k: r[k] for k in r.keys()})
        mid = enriched["match_id"]
        wd = parse_weekday(mid)
        key = wd if wd else "other"
        if key not in groups:
            groups[key] = []
        groups[key].append(enriched)
    
    result = []
    for wd in WEEKDAY_CN:
        if wd in groups:
            result.append({"sale_date": wd, "matches": groups[wd]})
    if "other" in groups:
        result.append({"sale_date": "\u65e9\u671f", "matches": groups["other"]})
    
    return jsonify({"groups": result})

@app.route("/api/dashboard/prediction/<match_id>")
def prediction_detail(match_id):
    db = db_get()
    _build_result_cache(db)
    rid = db.execute("SELECT MAX(run_id) FROM matches").fetchone()[0]
    row = db.execute("SELECT * FROM matches WHERE run_id=? AND match_id=? ORDER BY id DESC LIMIT 1", (rid, match_id)).fetchone()
    db.close()
    if not row:
        return jsonify({"error": "match not found"}), 404
    data = {k: row[k] for k in row.keys()}
    data = enrich_row_with_results(data)
    for k in data:
        if isinstance(data[k], bytes):
            data[k] = data[k].decode("utf-8", errors="replace")
    return jsonify(data)

@app.route("/api/dashboard/review")
def review():
    db = db_get()
    _build_result_cache(db)
    rid = db.execute("SELECT MAX(run_id) FROM matches").fetchone()[0]
    
    all_rows = db.execute("SELECT match_id FROM matches WHERE run_id=?", (rid,)).fetchall()
    match_ids = [r["match_id"] for r in all_rows]
    
    # Build enriched completed list
    completed_raw = db.execute(
        "SELECT id, match_id, home, away, match_time, event, direction, rating, fit_score, actual_score, half_time_score, hit, diagnosis, result_updated_at FROM matches WHERE run_id=? ORDER BY id DESC",
        (rid,)
    ).fetchall()
    
    completed_list = []
    for r in completed_raw:
        d = enrich_row_with_results({k: r[k] for k in r.keys()})
        if d.get("actual_score"):
            completed_list.append(d)
    
    # Limit to 50
    completed_list = completed_list[:50]
    
    # Cross-run stats
    total_rated = 0; total_hit = 0
    for mid in match_ids:
        if mid in _RESULT_CACHE and _RESULT_CACHE[mid]["hit"] is not None:
            total_rated += 1
            if _RESULT_CACHE[mid]["hit"] == 1:
                total_hit += 1
    
    # Rating stats from cross-run
    rating_stats_map = {}
    for r in completed_raw:
        d = enrich_row_with_results({k: r[k] for k in r.keys()})
        rat = d.get("rating", "")
        if rat and d.get("hit") is not None:
            if rat not in rating_stats_map:
                rating_stats_map[rat] = {"total": 0, "hits": 0}
            rating_stats_map[rat]["total"] += 1
            if d["hit"] == 1:
                rating_stats_map[rat]["hits"] += 1
    
    rating_stats = [
        {"rating": k, "total": v["total"], "hits": v["hits"],
         "rate": round(v["hits"]/v["total"]*100, 1) if v["total"] else 0}
        for k, v in sorted(rating_stats_map.items())
    ]
    
    # Trend
    trend_map = {}
    for mid in match_ids:
        if mid in _RESULT_CACHE:
            h = _RESULT_CACHE[mid]["hit"]
            if h is not None:
                wd = parse_weekday(mid)
                key = wd if wd else "other"
                if key not in trend_map:
                    trend_map[key] = {"total": 0, "hit": 0}
                trend_map[key]["total"] += 1
                if h == 1:
                    trend_map[key]["hit"] += 1
    
    trend = []
    for wd in WEEKDAY_CN:
        if wd in trend_map:
            t = trend_map[wd]
            trend.append({"label": wd, "hit": t["hit"], "total": t["total"], "rate": round(t["hit"]/t["total"]*100, 1) if t["total"] else 0})
    if "other" in trend_map:
        t = trend_map["other"]
        trend.append({"label": "\u65e9\u671f", "hit": t["hit"], "total": t["total"], "rate": round(t["hit"]/t["total"]*100, 1) if t["total"] else 0})
    
    db.close()
    
    cumulative_rate = round(total_hit / total_rated * 100, 1) if total_rated else 0
    
    return jsonify({
        "completed": completed_list,
        "cumulative": {"total": total_rated, "hits": total_hit, "rate": cumulative_rate},
        "rating_stats": rating_stats,
        "trend": trend
    })


# ==================== Action endpoints ====================

@app.route("/api/dashboard/action/fetch_results")
def action_fetch_results():
    return jsonify({"msg": "赛果查询功能将在后续迭代中实现（fetch_results.py）"})

@app.route("/api/dashboard/action/fetch_jczq")
def action_fetch_jczq():
    return jsonify({"msg": "竞彩网数据获取将在后续迭代中实现（fetch_jczq.py）"})

@app.route("/api/dashboard/action/run_predict")
def action_run_predict():
    return jsonify({"msg": "预测管道将在后续迭代中实现（run_all.py）"})
@app.route("/api/dashboard/plan")
def plan_data():
    """Return plan_data.json for the dashboard plans panel."""
    import os, json
    plan_path = os.path.join(os.path.dirname(__file__), "data", "plan_data.json")
    if os.path.exists(plan_path):
        with open(plan_path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5021, debug=True)
