import sqlite3

db = sqlite3.connect("D:\\V3.3.3-Core\\framework.db")

# Get latest run_id for each match that has actual_score
rows = db.execute("""
    SELECT match_id, run_id, direction, actual_score, jc_handicap
    FROM matches
    WHERE actual_score IS NOT NULL AND actual_score != ""
    AND direction IS NOT NULL AND direction != ""
    ORDER BY match_id, run_id DESC
""").fetchall()

updated = 0
seen = set()
for r in rows:
    mid = r[0]
    if mid in seen:
        continue
    seen.add(mid)
    
    score = r[3]
    direction = r[2]
    handicap = int(r[4] or 0)
    
    if ":" not in score:
        continue
    
    parts = score.split(":")
    hg, ag = int(parts[0]), int(parts[1])
    
    # Calculate hit
    if direction == "胜":
        hit = 1 if hg > ag else 0
    elif direction == "负":
        hit = 1 if hg < ag else 0
    elif direction == "平":
        hit = 1 if hg == ag else 0
    elif direction == "让胜":
        hit = 1 if (hg + handicap) > ag else 0
    elif direction == "让负":
        hit = 1 if (hg + handicap) < ag else 0
    elif direction == "让平":
        hit = 1 if (hg + handicap) == ag else 0
    else:
        hit = None
    
    if hit is not None:
        db.execute("UPDATE matches SET hit=? WHERE match_id=? AND run_id=?", (hit, mid, r[1]))
        updated += 1
        status = "HIT" if hit else "MISS"
        print(f'  {mid}: {direction} ({hg}:{ag}, hc={handicap}) -> {status}')

db.commit()
db.close()
print(f"\nUpdated {updated} matches")
