import json, sqlite3, os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "framework.db")
DATA_DIR = os.path.join(BASE_DIR, "data")

def main():
    # Load wc_schedule.json
    wc_path = os.path.join(DATA_DIR, "wc_schedule.json")
    if not os.path.exists(wc_path):
        print("ERROR: wc_schedule.json not found")
        return
    
    wc = json.load(open(wc_path, "r", encoding="utf-8"))
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    
    updated = 0
    inserted = 0
    
    for m in wc["matches"]:
        odds = m.get("odds") or {}
        mid = odds.get("id", "")
        if not mid:
            # Generate match_id if odds not available
            continue
        
        # Build match date from date+time
        md = m.get("date", "")
        mt = m.get("time", "")
        match_date_str = md
        match_time_str = md + " " + mt
        
        # Find existing match records (latest run_id)
        existing = cur.execute(
            "SELECT id, run_id FROM matches WHERE match_id=? ORDER BY run_id DESC LIMIT 1",
            (mid,)
        ).fetchone()
        
        if existing:
            # Update with WC data
            cur.execute("""
                UPDATE matches SET
                    wc_group=?, match_date=?,
                    jc_sp_home=?, jc_sp_draw=?, jc_sp_away=?,
                    ah_home=?, ah_draw=?, ah_away=?
                WHERE id=?
            """, (
                m.get("group", ""), match_date_str,
                _parse_float(odds.get("sp_h")),
                _parse_float(odds.get("sp_d")),
                _parse_float(odds.get("sp_a")),
                _parse_float(odds.get("hh_h")),
                _parse_float(odds.get("hh_d")),
                _parse_float(odds.get("hh_a")),
                existing[0]
            ))
            updated += 1
        else:
            # Insert new record (no prediction data yet)
            cur.execute("""
                INSERT INTO matches (
                    run_id, match_id, home, away, event, match_time, match_type,
                    wc_group, match_date,
                    jc_sp_home, jc_sp_draw, jc_sp_away,
                    ah_home, ah_draw, ah_away
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                1, mid, m.get("home",""), m.get("away",""),
                "世界杯", match_time_str, "世界杯",
                m.get("group", ""), match_date_str,
                _parse_float(odds.get("sp_h")),
                _parse_float(odds.get("sp_d")),
                _parse_float(odds.get("sp_a")),
                _parse_float(odds.get("hh_h")),
                _parse_float(odds.get("hh_d")),
                _parse_float(odds.get("hh_a")),
            ))
            inserted += 1
    
    conn.commit()
    conn.close()
    print(f"Updated: {updated}, Inserted: {inserted}")

def _parse_float(v):
    if v is None:
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None

if __name__ == "__main__":
    main()
