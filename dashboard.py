import json, os, sys
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

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/dashboard/stats")
def stats():
    db = db_get()
    total = db.execute("SELECT COUNT(*) FROM matches").fetchone()[0]
    scored = db.execute("SELECT COUNT(*) FROM matches WHERE actual_score IS NOT NULL AND actual_score != ''").fetchone()[0]
    predicted = db.execute("SELECT COUNT(*) FROM matches WHERE direction IS NOT NULL AND direction != ''").fetchone()[0]
    hit = db.execute("SELECT COUNT(*) FROM matches WHERE hit = 1").fetchone()[0]
    miss = db.execute("SELECT COUNT(*) FROM matches WHERE hit = 0").fetchone()[0]
    today = db.execute("SELECT match_id FROM matches WHERE direction IS NULL OR direction = '' ORDER BY match_id").fetchall()
    recent = db.execute("SELECT match_id, home, away, match_time, event, direction, rating, actual_score, hit, fit_score FROM matches ORDER BY match_id DESC LIMIT 20").fetchall()
    db.close()
    recent_list = [{k: r[k] for k in r.keys()} for r in recent]
    analysis = load_json(os.path.join(APP_DATA, "analysis.json"))
    al = list(analysis.get("AL", {}).keys()) if analysis else []
    return jsonify({"total": total, "scored": scored, "predicted": predicted, "hit": hit, "miss": miss, "today_need_predict": len(today), "al_groups": al, "recent": recent_list})

@app.route("/api/dashboard/matches")
def matches():
    db = db_get()
    rows = db.execute("SELECT match_id, home, away, match_time, event, direction, rating, actual_score, hit, fit_score, half_full, jc_sp_home, jc_sp_draw, jc_sp_away, jc_handicap FROM matches ORDER BY match_id").fetchall()
    db.close()
    return jsonify([{k: r[k] for k in r.keys()} for r in rows])

@app.route("/api/dashboard/analysis")
def analysis():
    data = load_json(os.path.join(APP_DATA, "analysis.json"))
    if not data:
        return jsonify({"error": "no analysis.json"})
    ratings = data.get("rating", [])
    return jsonify({"total_ratings": len(ratings), "completed": len([r for r in ratings if r.get("actual_score")]), "predicted": len([r for r in ratings if r.get("direction") and not r.get("actual_score")]), "waiting": len([r for r in ratings if not r.get("direction")]), "al_keys": list(data.get("AL", {}).keys())})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5021, debug=True)
