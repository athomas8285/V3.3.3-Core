import sqlite3
conn = sqlite3.connect(r"C:\Users\gjj\Desktop\v333\framework.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Check match_id / index field in matches
cur.execute("PRAGMA table_info(matches)")
cols = cur.fetchall()
for c in cols:
    print(f"  {c[1]} ({c[2]})")

print("\n--- All match_ids ---")
cur.execute("SELECT match_id, run_id FROM matches ORDER BY run_id, match_id")
for r in cur.fetchall():
    print(f"  run_id={r['run_id']}  match_id={r['match_id']}")

print("\n--- runs with their matches ---")
cur.execute("""
    SELECT r.id, r.date, r.run_type, r.total_matches, r.hit_count, m.match_id, m.home, m.away, m.league, m.direction, m.actual_score, m.hit
    FROM runs r
    LEFT JOIN matches m ON m.run_id = r.id
    ORDER BY r.date DESC, m.match_id
""")
rows = cur.fetchall()
current_run = None
for r in rows:
    if r["id"] != current_run:
        print(f"\n=== run_id={r['id']}  date={r['date']}  type={r['run_type']}  total={r['total_matches']} hit={r['hit_count']} ===")
        current_run = r["id"]
    if r["match_id"]:
        hit_mark = "✅" if r["hit"] else ("❌" if r["hit"] == 0 else "?")
        print(f"  {r['match_id']}: {r['home']} vs {r['away']} | {r['league']} | {r['direction']} | {r['actual_score'] or '-'} {hit_mark}")
