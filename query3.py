import sqlite3
conn = sqlite3.connect(r"C:\Users\gjj\Desktop\v333\framework.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get runs with dates
cur.execute("SELECT id, date, run_type, total_matches, hit_count, created_at, prediction_date FROM runs ORDER BY id")
runs = cur.fetchall()
for r in runs:
    print(f"run_id={r['id']}  date={r['date']}  type={r['run_type']}  total={r['total_matches']}  hit={r['hit_count']}  pred_date={r['prediction_date']}")

print()

# Get matches per run with match_id
cur.execute("""
    SELECT r.id as run_id, r.date, m.match_id, m.home, m.away, m.league, m.direction, m.actual_score, m.hit, m.rating
    FROM runs r
    LEFT JOIN matches m ON m.run_id = r.id
    ORDER BY r.id, m.match_id
""")
rows = cur.fetchall()
for r in rows:
    hit_str = "Y" if r["hit"] == 1 else ("N" if r["hit"] == 0 else "?")
    score = r["actual_score"] or "-"
    print(f"run={r['run_id']} date={r['date']}  #{r['match_id']}: {r['home']} vs {r['away']} | {r['league']} | {r['direction']} | {score} {hit_str}")

conn.close()
