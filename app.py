# app.py
import subprocess, json, os, sys, csv, traceback, threading
import track_odds
from flask import Flask, request, jsonify, Response
import database as db
from parser import main as parse_main

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
db.init_db()
# -- Odds background updater --
_last_odds_fetch = 0
_ODDS_INTERVAL = 1800  # 30 min

def _odds_scheduler():
    global _last_odds_fetch
    import time
    while True:
        now = time.time()
        if now - _last_odds_fetch >= _ODDS_INTERVAL:
            _last_odds_fetch = now
            try:
                n, _, u = track_odds.run()
                print('[Odds] Auto-update: %d matches, %d changes' % (n, u))
            except Exception as e:
                print('[Odds] Auto-update error: %s' % e)
        time.sleep(60)

def start_odds_scheduler():
    t = threading.Thread(target=_odds_scheduler, daemon=True)
    t.start()
    print('[Odds] Background updater started (30min interval)')



@app.route('/')
def index():
    import sqlite3
    import json as _json
    base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base, 'data')
    html = open(os.path.join(base, 'templates', 'index.html'), 'r', encoding='utf-8').read()
    try:
        info_list = _json.load(open(os.path.join(data_dir, 'match_info.json'), encoding='utf-8'))['matches']
        try:
            locked = _json.load(open(os.path.join(data_dir, 'locked_data.json'), encoding='utf-8'))
            locked_matches = locked.get('matches', []) if isinstance(locked, dict) else []
            hcap_map = {}
            for lm in locked_matches:
                hcap_map[lm.get("id","")] = {
                    "jc_hhad_win": lm.get("jc_hhad_win"),
                    "jc_hhad_draw": lm.get("jc_hhad_draw"),
                    "jc_hhad_lose": lm.get("jc_hhad_lose"),
                    "jc_handicap": lm.get("jc_handicap"),
                }
            for info_item in info_list:
                mid = info_item.get("id", "")
                if mid in hcap_map:
                    hcap = hcap_map[mid]
                    info_item["jc_hhad_win"] = hcap.get("jc_hhad_win")
                    info_item["jc_hhad_draw"] = hcap.get("jc_hhad_draw")
                    info_item["jc_hhad_lose"] = hcap.get("jc_hhad_lose")
                    info_item["jc_handicap"] = hcap.get("jc_handicap")
        except:
            pass
        data = {
            'rating': _json.load(open(os.path.join(data_dir, 'rating_result.json'), encoding='utf-8'))['matches'],
            'mc': _json.load(open(os.path.join(data_dir, 'monte_carlo_result.json'), encoding='utf-8'))['matches'],
            'info': info_list,
            'ddi': _json.load(open(os.path.join(data_dir, 'ddi_result.json'), encoding='utf-8'))['matches'],
            'ai': _json.load(open(os.path.join(data_dir, 'ai_judgment.json'), encoding='utf-8'))['matches'],
            'fit': _json.load(open(os.path.join(data_dir, 'fit_score_result.json'), encoding='utf-8'))['matches'],
            'trend': list(_json.load(open(os.path.join(data_dir, 'trend_features.json'), encoding='utf-8'))['matches'].values()),
        }

        # Merge DB results into rating data
        try:
            _conn = sqlite3.connect(os.path.join(base, "framework.db"))
            _cur = _conn.cursor()
            sql = "WITH latest AS (SELECT match_id, MAX(run_id) as max_run FROM matches WHERE actual_score IS NOT NULL GROUP BY match_id) SELECT m.match_id, m.actual_score, m.hit, m.half_full FROM matches m JOIN latest l ON m.match_id = l.match_id AND m.run_id = l.max_run"
            _cur.execute(sql)
            _db_rows = {r[0]: {"actual_score": r[1], "hit": bool(r[2]), "half_full": r[3] or ""} for r in _cur.fetchall()}
            _conn.close()
            for _rm in data["rating"]:
                _mid = _rm.get("id", "")
                if _mid in _db_rows:
                    _rm["actual_score"] = _db_rows[_mid]["actual_score"]
                    _rm["hit"] = _db_rows[_mid]["hit"]
                    _rm["half_full"] = _db_rows[_mid]["half_full"]
        except Exception as _e:
            pass

        # Build narratives

        try:
            _oh = _json.load(open(os.path.join(data_dir, 'odds_history', 'odds_history.json'), encoding='utf-8'))
        except:
            _oh = {}
        _rating_map = {m['id']: m for m in data['rating']}
        _mc_map = {m['id']: m for m in data['mc']}
        _ddi_map = {m['id']: m for m in data['ddi']}
        _ai_map = {m['id']: m for m in data['ai']}
        _fit_map = {m['id']: m for m in data['fit']}
        _narratives = {}
        for _m in info_list:
            _mid = _m.get('id', '')
            _mc = _mc_map.get(_mid, {})
            _ddi = _ddi_map.get(_mid, {})
            _ai = _ai_map.get(_mid, {})
            _fit = _fit_map.get(_mid, {})
            _home = _m.get('home', '')
            _away = _m.get('away', '')
            _parts = []
            # Direction + prob + lambda
            _phys = _mc.get('physical', {}) if _mc else {}
            _ph = _phys.get('home_win', 0)
            _pa = _phys.get('away_win', 0)
            _ld = _mc.get('lambda_diff') if _mc else None
            if _ph > _pa + 0.03:
                _dir = '主胜'
            elif _pa > _ph + 0.03:
                _dir = '客胜'
            else:
                _dir = '平局'
            _pl = '模型' + _dir + ' ' + str(round(_ph * 100, 1)) + '%'
            if _ld is not None:
                _pl += ' / 差' + ('+' if _ld >= 0 else '') + str(round(_ld, 2))
            _parts.append(_pl)
            # Trend
            _ohm = None
            for _ohid, _ohd in _oh.items():
                if _ohd.get('home') == _home and _ohd.get('away') == _away:
                    _ohm = _ohd
                    break
            if _ohm:
                _hhad = _ohm.get('tracks', {}).get('hhad', [])
                if len(_hhad) >= 2:
                    _count = len(_hhad)
                    _lower = _hhad[-1].get('h', 0) < _hhad[0].get('h', 0)
                    _dw = '压低主胜' if _lower else '推高主胜'
                    _parts.append('赔率趋势自' + str(int(_hhad[0]['ts'][5:7]))+'月'+str(int(_hhad[0]['ts'][8:10]))+'日' + '起连续' + str(_count) + '次' + _dw)
            # Market
            _sp = _m.get('sp_home')
            if _sp:
                _parts.append('方向与模型一致')
                _parts.append('市场同样看好' + ('主胜' if _ph > _pa + 0.03 else '客胜'))
            # DDI
            _dd = (_ddi.get('ddi', {}) if _ddi else {}).get('home_win', 0)
            if abs(_dd) > 0.06 and _dd < 0:
                _parts.append('不过市场预期显著高于物理模型')
                _parts.append('DDI 偏差 ' + str(round(_dd * 100, 1)) + '%')
                _parts.append('存在过度追捧可能')
            # Missing data
            _miss = []
            if _m.get('xg_season_missing') and _m.get('xg_last3_missing'): _miss.append('xG')
            if _m.get('h2h_missing'): _miss.append('交锋')
            if _m.get('roster_missing'): _miss.append('阵容')
            if _m.get('injury_home_missing') and _m.get('injury_away_missing'): _miss.append('伤停')
            _ft = (_fit.get('fit_score', {}) if _fit else {}).get('final_total', 0)
            if _miss or (_ft and _ft < 7):
                if _miss: _parts.append('且数据层面大面积缺失')
                if _ft: _parts.append('拟合分仅 ' + str(round(_ft, 1)))
                _parts.append('容错空间有限')
            # Verdict
            _hcap = _m.get('jc_handicap', 0)
            if _hcap and abs(_hcap) > 0:
                _deep = abs(_hcap) >= 1.5
                _med = abs(_hcap) >= 1.0
                _v = '方向' + _dir + '可关注'
                if _ph > _pa + 0.03:
                    if _deep:
                        _v += '，但让球盘穿盘难度较大，谨慎对待'
                    elif _med:
                        _v += '，让球盘需谨慎'
                elif _pa > _ph + 0.03:
                    if _deep:
                        _v += '，但受让盘需谨慎'
                _parts.append(_v)
            # Build paragraph
            if len(_parts) >= 2:
                _narratives[_mid] = '，'.join(_parts[:-1]) + '。' + _parts[-1] + '。'
            elif _parts:
                _narratives[_mid] = _parts[0] + '。'
        data['narratives'] = _narratives
        inline = '<script>var __DATA=' + _json.dumps(data) + ';</script>'
        html = html.replace('</head>', inline + '</head>')
    except:
        pass
    return html


@app.route('/api/latest')
def get_latest():
    import os as _os, json as _json
    def _load(name):
        path = _os.path.join(DATA_DIR, name + ".json")
        if _os.path.exists(path):
            try:
                return _json.load(open(path, encoding="utf-8")).get("matches", [])
            except:
                return []
        return []

    info_list  = _load("match_info")
    rating_list = _load("rating_result")
    ddi_list   = _load("ddi_result")
    mc_list    = _load("monte_carlo_result")
    ai_list    = _load("ai_judgment")

    def _idx(arr):
        return {m.get("id"): m for m in arr if m.get("id")}

    rating_idx = _idx(rating_list)
    ddi_idx    = _idx(ddi_list)
    mc_idx     = _idx(mc_list)
    ai_idx     = _idx(ai_list)

    matches = []
    reviews = []

    # determine date from first match
    today_str = ""
    for m in info_list:
        t = (m.get("time") or "")[:10]
        if t:
            today_str = t
            break

    for info in info_list:
        mid = info.get("id") or ""
        rat = rating_idx.get(mid, {})
        ddi = ddi_idx.get(mid, {})
        mc  = mc_idx.get(mid, {})
        ai  = ai_idx.get(mid, {})

        base = {
            "match_id": mid,
            "time": info.get("time", ""),
            "home": info.get("home", ""),
            "away": info.get("away", ""),
            "event": info.get("event", ""),
            "direction": rat.get("direction", ""),
            "fit_score": rat.get("fit_score"),
            "rating": rat.get("rating", ""),
            "lambda_diff": mc.get("lambda_diff"),
            "ddi_home_win": (ddi.get("ddi") or {}).get("home_win") if ddi.get("ddi") else None,
            "top2_total_goals": mc.get("top2_total_goals") if isinstance(mc.get("top2_total_goals"), list) else [],
            "top2_half_full": mc.get("top2_half_full") if isinstance(mc.get("top2_half_full"), list) else [],
            "top3_scores": mc.get("top3_scores") if isinstance(mc.get("top3_scores"), list) else [],
        }

        # build warning text
        warns = []
        if rat.get("direction_warning"):
            warns.append("方向存疑")
        if rat.get("meltdown"):
            warns.append("模型熔断")
        if ai and ai.get("trap_analysis"):
            warns.append(ai["trap_analysis"])
        if warns:
            base["warning"] = " | ".join(warns)

        # always treat today's matches as 'matches' (no actual_score yet)
        matches.append(base)

    # inject actual_score and hit from DB (JSON files are unreliable for these)
    try:
        _conn = db.get_db()
        _cur = _conn.cursor()
        _cur.execute("WITH _latest AS (SELECT match_id, MAX(run_id) as _mr FROM matches WHERE actual_score IS NOT NULL AND actual_score != '' GROUP BY match_id) SELECT m.match_id, m.actual_score, m.hit, m.half_full FROM matches m JOIN _latest l ON m.match_id = l.match_id AND m.run_id = l._mr")
        _rows = {r[0]: {"actual_score": r[1], "hit": bool(r[2]), "half_full": r[3] or ""} for r in _cur.fetchall()}
        _conn.close()
        for _m in matches:
            _mid = _m.get("match_id", "")
            if _mid in _rows:
                _m["actual_score"] = _rows[_mid]["actual_score"]
                _m["hit"] = _rows[_mid]["hit"]
                _m["half_full"] = _rows[_mid]["half_full"]
    except Exception as _e:
        pass

    # load reviews from history.csv
    import csv as _csv
    csv_path = _os.path.join(_os.path.dirname(DATA_DIR), "history.csv")
    if _os.path.exists(csv_path):
        try:
            with open(csv_path, "r", encoding="utf-8-sig") as _f:
                for _row in _csv.DictReader(_f):
                    _actual = (_row.get("actual_score") or "").strip()
                    if not _actual or "-" not in _actual:
                        continue
                    _rev = {
                        "match_id": _row.get("id", ""),
                        "time": _row.get("date", "")[:16],
                        "home": _row.get("home", ""),
                        "away": _row.get("away", ""),
                        "direction": _row.get("direction", ""),
                        "actual_score": _actual,
                        "hit": 1 if _row.get("hit") == "True" else 0,
                        "fit_score": float(_row["fit_score"]) if _row.get("fit_score") else None,
                        "rating": _row.get("rating", ""),
                        "half_full": _row.get("actual_ht", ""),
                        "lambda_diff": float(_row["lambda_final_h"]) - float(_row["lambda_final_a"]) if _row.get("lambda_final_h") and _row.get("lambda_final_a") else None,
                        "diagnosis": _row.get("diagnosis", ""),
                    }
                    _ddi_h = _row.get("ddi_home", "")
                    if _ddi_h:
                        try:
                            _rev["ddi_home_win"] = float(_ddi_h)
                        except:
                            pass
                    reviews.append(_rev)
        except:
            pass

    total = len(reviews)
    hits = sum(1 for r in reviews if r.get("hit"))
    hit_rate = round(hits / total * 100, 1) if total else 0

    return jsonify({
        "matches": matches,
        "reviews": reviews,
        "date": today_str,
        "total": total,
        "hits": hits,
        "hit_rate": hit_rate,
    })


def _check_hit(direction, actual_score):
    """Simple check if predicted direction matches actual result."""
    if not direction or not actual_score:
        return False
    try:
        parts = actual_score.split("-")
        h, a = int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        return False
    if direction in ("胜", "主胜", "home"):
        return h > a
    if direction in ("负", "客胜", "away"):
        return a > h
    if direction in ("平", "平局", "draw"):
        return h == a
    return False

@app.route('/api/parse', methods=['POST'])
def parse_raw():
    text = request.json.get('text', '')
    if not text:
        return jsonify({'error': '\u8bf7\u8f93\u5165\u539f\u59cb\u6570\u636e\u6587\u672c'}), 400
    try:
        result = parse_main(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': '\u89e3\u6790\u5931\u8d25: ' + str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    factors = data.get('factor_params')
    if not factors:
        return jsonify({'error': '\u7f3a\u5c11 factor_params'}), 400
    try:
        with open(os.path.join(DATA_DIR, 'factor_params.json'), 'w', encoding='utf-8') as f:
            json.dump(factors, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return jsonify({'error': '\u6587\u4ef6\u4fdd\u5b58\u5931\u8d25: ' + str(e)}), 500
    try:
        result = subprocess.run([sys.executable, 'run_all.py'], cwd=BASE_DIR, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            return jsonify({'error': '\u5206\u6790\u5931\u8d25:\n' + (result.stderr[-800:] or result.stdout[-800:])}), 500
    except subprocess.TimeoutExpired:
        return jsonify({'error': '\u5206\u6790\u8d85\u65f6'}), 500
    try:
        rating = json.load(open(os.path.join(DATA_DIR, 'rating_result.json'), encoding='utf-8'))
        mc = json.load(open(os.path.join(DATA_DIR, 'monte_carlo_result.json'), encoding='utf-8'))
        info = json.load(open(os.path.join(DATA_DIR, 'match_info.json'), encoding='utf-8'))
        ddi_data = json.load(open(os.path.join(DATA_DIR, 'ddi_result.json'), encoding='utf-8'))
        ai_data = json.load(open(os.path.join(DATA_DIR, 'ai_judgment.json'), encoding='utf-8'))
        return jsonify({
            'rating': rating['matches'], 'mc': mc['matches'], 'info': info['matches'],
            'ddi': ddi_data['matches'], 'ai': ai_data['matches']
        })
    except Exception as e:
        return jsonify({'error': '\u7ed3\u679c\u8bfb\u53d6\u5931\u8d25: ' + str(e)}), 500


@app.route('/api/review', methods=['POST'])
def review():
    scores = request.json.get('scores', [])
    if not scores:
        return jsonify({'error': '\u65e0\u590d\u76d8\u6570\u636e'}), 400
    with open(os.path.join(DATA_DIR, 'review.json'), 'w', encoding='utf-8') as f:
        json.dump({'matches': scores}, f, ensure_ascii=False, indent=2)
    try:
        subprocess.run([sys.executable, 'review.py'], cwd=BASE_DIR, capture_output=True, text=True, timeout=60)
        history_path = os.path.join(BASE_DIR, 'history.csv')
        reviews = []
        if os.path.exists(history_path):
            with open(history_path, 'r', encoding='utf-8-sig') as f:
                for row in csv.DictReader(f):
                    if row.get('actual_score'):
                        reviews.append({
                            'id': row['id'], 'home': row['home'], 'away': row['away'],
                            'direction': row.get('direction', ''), 'actual_score': row['actual_score'],
                            'hit': row.get('hit', ''), 'diagnosis': row.get('diagnosis', '')
                        })
        hit_count = sum(1 for r in reviews if r.get('hit') == 'True')
        total = len(reviews)
        round_reviews = [r for r in reviews if r['id'] in [s['id'] for s in scores]]
        round_hit = sum(1 for r in round_reviews if r.get('hit') == 'True')
        round_total = len(round_reviews)
        return jsonify({
            'reviews': reviews,
            'stats': {
                'total': total, 'hit': hit_count,
                'round_total': round_total, 'round_hit': round_hit
            }
        })
    except Exception as e:
        return jsonify({'error': '\u590d\u76d8\u5931\u8d25: ' + str(e)}), 500




@app.route('/api/reviews')
def get_reviews():
    import csv
    path = os.path.join(BASE_DIR, "history.csv")
    reviews = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                if row.get("actual_score"):
                    mid = row["id"]
                    mdate = row.get("date", "")[:10]
                    pd = {}
                    try:
                        conn = db.get_db()
                        r = conn.execute("SELECT r.prediction_date,m.top2_total_goals,m.top2_half_full,m.top3_scores,m.lambda_diff,m.ddi_home_win,m.fit_score,m.rating,m.scenario_type FROM matches m JOIN runs r ON m.run_id=r.id WHERE m.match_id=? AND m.home=? AND m.away=? AND r.date<=? ORDER BY r.id DESC LIMIT 1", (mid, row["home"], row["away"], mdate)).fetchone()
                        if r:
                            pd = dict(r)
                        conn.close()
                    except:
                        pass
                    reviews.append({
                        "id": mid, "date": row.get("date", ""),
                        "prediction_date": pd.get("prediction_date"),
                        "home": row["home"], "away": row["away"],
                        "direction": row.get("direction", ""),
                        "actual_score": row["actual_score"],
                        "hit": row.get("hit", ""),
                        "diagnosis": row.get("diagnosis", ""),
                        "actual_ht": row.get("actual_ht", ""),
                        "top2_total_goals": pd.get("top2_total_goals"),
                        "top2_half_full": pd.get("top2_half_full"),
                        "top3_scores": pd.get("top3_scores"),
                        "lambda_diff": pd.get("lambda_diff"),
                        "ddi_home_win": pd.get("ddi_home_win"),
                        "fit_score": pd.get("fit_score"),
                        "rating": pd.get("rating"),
                        "scenario_type": pd.get("scenario_type")
                    })
    return jsonify(reviews[-50:])
@app.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/test')
def test_page():
    with open(os.path.join(BASE_DIR, 'templates', 'test.html'), 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/full_test')
def full_test():
    with open(os.path.join(BASE_DIR, 'templates', 'full_test.html'), 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/debug')
def debug_page():
    with open(os.path.join(BASE_DIR, 'templates', 'debug.html'), 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/charts.js')
def charts_js():
    from flask import Response
    with open(os.path.join(BASE_DIR, 'templates', 'charts.js'), 'r', encoding='utf-8') as f:
        return Response(f.read(), mimetype='application/javascript')


@app.route('/live.js')
def live_js():
    from flask import Response
    with open(os.path.join(BASE_DIR, 'templates', 'live.js'), 'r', encoding='utf-8') as f:
        return Response(f.read(), mimetype='application/javascript')

@app.route('/sw.js')
def sw_js():
    from flask import Response
    with open(os.path.join(BASE_DIR, 'static', 'sw.js'), 'r', encoding='utf-8') as f:
        return Response(f.read(), mimetype='application/javascript')





@app.route('/v1')
def v1_compare():
    with open(os.path.join(BASE_DIR, 'templates', 'v1.html'), 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/v2')
def v2_compare():
    with open(os.path.join(BASE_DIR, 'templates', 'v2.html'), 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/v3')
def v3_compare():
    with open(os.path.join(BASE_DIR, 'templates', 'v3.html'), 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/v4')
def v4_edit():
    with open(os.path.join(BASE_DIR, 'templates', 'v4.html'), 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/v5')
def v5_edit():
    with open(os.path.join(BASE_DIR, 'templates', 'v5.html'), 'r', encoding='utf-8') as f:
        return f.read()
def v4_edit():
    with open(os.path.join(BASE_DIR, 'templates', 'v4.html'), 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/wc21')
def wc21_page():
    with open(os.path.join(BASE_DIR, 'templates', 'wc21.html'), 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/wc22')
def wc22_page():
    with open(os.path.join(BASE_DIR, 'templates', 'wc22.html'), 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/wc23')
def wc23_page():
    with open(os.path.join(BASE_DIR, 'templates', 'wc23.html'), 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/wc24')
def wc24_page():
    with open(os.path.join(BASE_DIR, 'templates', 'wc24.html'), 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/live/recalibrate', methods=['POST'])



def live_recalibrate():
    import sys
    sys.path.insert(0, BASE_DIR)
    from live_ddi import recalibrate, load_current
    data = request.json
    if not data or "matches" not in data:
        return jsonify({"error": "need matches field"}), 400
    results = []
    current_data = load_current()
    for m in data["matches"]:
        mid = str(m["mid"])
        try:
            result = recalibrate(mid, float(m["sp_home"]), float(m["sp_draw"]), float(m["sp_away"]),
                                 starting_lineup_confirmed=m.get("lineup_confirmed"), data=current_data)
            results.append(result)
        except Exception as e:
            results.append({"match_id": mid, "error": str(e)})
    return jsonify({"results": results})

@app.route("/api/live/info")
def live_info():
    import sys
    sys.path.insert(0, BASE_DIR)
    from live_ddi import load_current
    data = load_current()
    matches = []
    for mid in sorted(data["info"].keys()):
        info = data["info"][mid]
        rating = data["rating"].get(mid, {})
        matches.append({
            "id": mid, "home": info["home"], "away": info["away"],
            "event": info.get("event", ""), "time": info.get("time", ""),
            "sp_home": info["sp_home"], "sp_draw": info["sp_draw"], "sp_away": info["sp_away"],
            "init_sp_home": info.get("initial_sp_home", info["sp_home"]),
            "init_sp_draw": info.get("initial_sp_draw", info["sp_draw"]),
            "init_sp_away": info.get("initial_sp_away", info["sp_away"]),
            "direction": rating.get("direction", ""),
            "fit_score": rating.get("fit_score", 0),
            "rating": rating.get("rating", ""),
        })
    return jsonify({"matches": matches})



@app.route('/api/wc-matches')
def wc_matches():
    """Return all World Cup matches with prediction data and odds from DB."""
    conn = db.get_db()
    cur = conn.cursor()
    # Get latest run_id for each WC match (match_id starting with weekday)
    cur.execute("""
        WITH latest AS (
            SELECT match_id, MAX(run_id) as max_run
            FROM matches
            WHERE match_id IN (
                SELECT match_id FROM matches 
                WHERE match_id GLOB '*[\u4e00-\u9fff]*[0-9]'
            )
            GROUP BY match_id
        )
        SELECT m.* FROM matches m
        JOIN latest l ON m.match_id = l.match_id AND m.run_id = l.max_run
        ORDER BY m.match_time
    """)
    cols = [d[0] for d in cur.description]
    rows = []
    for row in cur.fetchall():
        d = dict(zip(cols, row))
        # Parse JSON fields
        for f in ('top2_total_goals', 'top2_half_full', 'top3_scores'):
            if d.get(f):
                try:
                    d[f] = json.loads(d[f])
                except:
                    d[f] = []
        rows.append(d)
    conn.close()
    return jsonify({'matches': rows})

@app.route("/api/history/runs")
def history_runs():
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT prediction_date, total_matches, hit_count FROM runs ORDER BY prediction_date ASC")
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)







@app.route("/api/history/matches")
def history_matches():
    date = request.args.get("date", "")
    if not date:
        return jsonify({"matches": []})
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT match_id, home, away, event, match_time, direction, fit_score, rating,
               actual_score, hit, lambda_diff, ddi_home_win, scenario_type,
               top2_total_goals, top2_half_full, top3_scores, half_time_score, half_full, diagnosis
        FROM matches m
        JOIN runs r ON r.id = m.run_id
        WHERE r.prediction_date = ?
        ORDER BY m.match_time
    """, (date,))

    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    return jsonify({"matches": rows})

@app.route('/api/v2/data')
def api_v2_data():
    import os as _os, json as _json
    base = _os.path.dirname(_os.path.abspath(__file__))
    data_dir = _os.path.join(base, 'data')
    def _load(name):
        path = _os.path.join(data_dir, name + '.json')
        if _os.path.exists(path):
            try: return _json.load(open(path, encoding='utf-8')).get('matches', [])
            except: return []
        return []
    rating_data = _load('rating_result')
    has_data = len(rating_data) > 0
    today_scan_status = 'ACTIVE' if has_data else 'IDLE'
    prediction_date = ''
    if has_data:
        rating_path = _os.path.join(data_dir, 'rating_result.json')
        try:
            from datetime import datetime as _dt
            prediction_date = _dt.fromtimestamp(_os.path.getmtime(rating_path)).strftime('%Y-%m-%d')
        except:
            pass
    return _json.dumps({
        'prediction_date': prediction_date,
        'today_scan': {
            'status': today_scan_status,
            'date': '2026-06-05',
            'message': '等待今日预测任务' if not has_data else '扫描完成'
        },
        'rating': rating_data,
        'mc': _load('monte_carlo_result'),
        'info': _load('match_info'),
        'ddi': _load('ddi_result'),
        'ai': _load('ai_judgment'),
    })





@app.route("/api/doc/sections")
def doc_sections():
    """Return documentation section metadata for sidebar."""
    sections = [
        {"id": "doc-params", "title": "核心参数说明", "icon": "🛠️", "type": "params"},
        {"id": "doc-arch", "title": "分析框架说明", "icon": "🏗️", "type": "arch"},
    ]
    return jsonify({"sections": sections})

@app.route("/api/doc/content/<doc_type>")
def doc_content(doc_type):
    """Return the raw markdown content for a documentation file."""
    file_map = {
        "params": "_doc_params.md",
        "arch": "_doc_framework.md",
    }
    filename = file_map.get(doc_type)
    if not filename:
        return jsonify({"error": "unknown doc type"}), 404
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "doc file not found"}), 404
    with open(filepath, "r", encoding="utf-8") as f:
        md_content = f.read()
    return Response(md_content, mimetype="text/plain; charset=utf-8")


@app.route('/api/odds/history')
def odds_history():
    try:
        hist_file = os.path.join(DATA_DIR, 'odds_history', 'odds_history.json')
        if os.path.exists(hist_file):
            with open(hist_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        return jsonify({})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/odds/refresh')
def odds_refresh():
    try:
        n, new_n, upd_n = track_odds.run()
        return jsonify({'ok': True, 'matches': n, 'new': new_n, 'updated': upd_n})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5020))
    debug = os.environ.get('FLASK_ENV', 'development') != 'production'
    start_odds_scheduler()
    app.run(host='0.0.0.0', port=port, debug=debug)


