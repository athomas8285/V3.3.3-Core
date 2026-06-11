# trend_features.py
# V3.3.3-Core-Rev1.15 odds trend feature extraction

import json, os, statistics
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ODDS_HISTORY_FILE = os.path.join(BASE_DIR, "data", "odds_history", "odds_history.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "trend_features.json")

TS_FMT = "%Y-%m-%dT%H:%M"

def parse_ts(ts_str):
    return datetime.strptime(ts_str, TS_FMT)

def load_odds_history():
    if not os.path.exists(ODDS_HISTORY_FILE):
        return {}
    with open(ODDS_HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def compute_hhad_trends(tracks):
    hhad = tracks.get("hhad", [])
    if len(hhad) < 2:
        return None, None
    records = sorted(hhad, key=lambda x: x["ts"])
    first, last = records[0], records[-1]
    h_delta = last.get("h", 0) - first.get("h", 0)
    d_delta = last.get("d", 0) - first.get("d", 0)
    a_delta = last.get("a", 0) - first.get("a", 0)
    t0 = parse_ts(first["ts"])
    t1 = parse_ts(last["ts"])
    days_span = max((t1 - t0).total_seconds() / 86400, 0.01)
    h_velocity = h_delta / days_span
    a_velocity = a_delta / days_span
    fh = h_delta < -0.05 and a_delta > 0.05
    fa = a_delta < -0.05 and h_delta > 0.05
    stable = abs(h_delta) < 0.05 and abs(a_delta) < 0.05
    dv = (h_delta < -0.05 and a_delta > 0.05) or (a_delta < -0.05 and h_delta > 0.05)
    mx = (h_delta < -0.05 and a_delta < -0.05) or (h_delta > 0.05 and a_delta > 0.05)
    if fh: direction = "favors_home"
    elif fa: direction = "favors_away"
    elif stable: direction = "stable"
    elif dv: direction = "divergent"
    elif mx: direction = "mixed"
    else: direction = "stable"
    late_acc = False
    if len(records) >= 3:
        mid = len(records) // 2
        fh2 = records[:mid]
        sh = records[mid:]
        if len(fh2) >= 1 and len(sh) >= 1:
            er = abs(fh2[-1].get("h", 0) - fh2[0].get("h", 0)) / max(days_span * 0.5, 0.01)
            lr = abs(sh[-1].get("h", 0) - sh[0].get("h", 0)) / max(days_span * 0.5, 0.01)
            if lr > er * 1.5 and lr > 0.05:
                late_acc = True
    deltas_h = []
    for i in range(1, len(records)):
        deltas_h.append(records[i].get("h", 0) - records[i-1].get("h", 0))
    consistency = 1.0
    if deltas_h:
        try:
            sd = statistics.stdev(deltas_h)
            if sd < 0.05:
                consistency = round(1.0 - min(sd * 5, 0.3), 2)
            else:
                consistency = round(max(0.5, 1.0 - min(sd * 3, 0.5)), 2)
        except statistics.StatisticsError:
            consistency = 1.0
    features = {
        "change_count": len(records),
        "h_delta": round(h_delta, 4), "d_delta": round(d_delta, 4), "a_delta": round(a_delta, 4),
        "days_span": round(days_span, 2),
        "velocity_per_day": round(h_velocity, 4), "away_velocity_per_day": round(a_velocity, 4),
        "direction": direction, "late_acceleration": late_acc, "consistency": consistency,
    }
    summary = {"change_count": len(records), "direction": direction, "late_acceleration": late_acc,
               "h_velocity": round(h_velocity, 4), "a_velocity": round(a_velocity, 4)}
    return features, summary

def compute_had_trends(tracks):
    had = tracks.get("had", [])
    if len(had) < 2:
        return None, None
    records = sorted(had, key=lambda x: x["ts"])
    first, last = records[0], records[-1]
    h_delta = last.get("h", 0) - first.get("h", 0)
    a_delta = last.get("a", 0) - first.get("a", 0)
    t0 = parse_ts(first["ts"])
    t1 = parse_ts(last["ts"])
    days_span = max((t1 - t0).total_seconds() / 86400, 0.01)
    h_velocity = h_delta / days_span
    if h_delta < -0.05 and a_delta > 0.05:
        direction = "favors_home"
    elif a_delta < -0.05 and h_delta > 0.05:
        direction = "favors_away"
    else:
        direction = "stable"
    features = {"change_count": len(records), "h_delta": round(h_delta, 4), "a_delta": round(a_delta, 4),
                "direction": direction, "velocity_per_day": round(h_velocity, 4)}
    summary = {"change_count": len(records), "direction": direction}
    return features, summary

def compute_overall_market_pressure(match_results):
    cmb = [m["combined"] for m in match_results.values() if m["combined"]]
    if not cmb:
        return {"market_pressure": "neutral", "pressure_strength": 0, "divergence_warning": False}
    directions = [c["direction"] for c in cmb]
    fh = directions.count("favors_home")
    fa = directions.count("favors_away")
    total = len(directions)
    hr = fh / total if total > 0 else 0
    ar = fa / total if total > 0 else 0
    late_cnt = sum(1 for c in cmb if c.get("late_acceleration", False))
    dw = hr > 0.5 and ar > 0.3
    if hr > 0.6:
        mp = "favors_home"; ps = hr
    elif ar > 0.6:
        mp = "favors_away"; ps = ar
    else:
        mp = "mixed"; ps = max(hr, ar)
    return {"market_pressure": mp, "pressure_strength": round(ps, 2),
            "divergence_warning": dw, "late_acceleration_count": late_cnt,
            "total_matches_with_trends": total}

def extract_trends():
    odds_data = load_odds_history()
    if not odds_data:
        print("  [WARN] odds_history.json not found or empty")
        return None
    match_results = {}
    for mid, mo in odds_data.items():
        home = mo.get("home", "")
        away = mo.get("away", "")
        tracks = mo.get("tracks", {})
        hhad_f, hhad_s = compute_hhad_trends(tracks)
        had_f, had_s = compute_had_trends(tracks)
        if hhad_s:
            combined = hhad_s
        elif had_s:
            combined = had_s
        else:
            combined = {"change_count": 0, "direction": "no_data", "late_acceleration": False}
        matchNum = mo.get("matchNum", "")
        match_results[mid] = {"home": home, "away": away,
            "matchNum": matchNum,
            "hhad": hhad_f, "had": had_f, "combined": combined}
    overall = compute_overall_market_pressure(match_results)
    match_num_index = {}
    for mid, mr in match_results.items():
        mn = mr.get("matchNum", "")
        if mn:
            match_num_index[mn] = mid
    result = {"matches": match_results, "overall": overall, "match_num_index": match_num_index}
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    wt = sum(1 for m in match_results.values() if m["combined"]["change_count"] >= 2)
    print("  [OK] trend_features done: {} matches, {} with >=2 rec".format(len(match_results), wt))
    print("       market: {} (str={})".format(overall["market_pressure"], overall["pressure_strength"]))
    return result

def main():
    print("=" * 55)
    print("  V3.3.3-Core-Rev1.15 odds trend feature extraction")
    print("=" * 55)
    extract_trends()

if __name__ == "__main__":
    main()