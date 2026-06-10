import sqlite3
conn = sqlite3.connect(r"C:\Users\gjj\Desktop\v333\framework.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT match_id, home, away, direction, actual_score, half_full, hit FROM matches WHERE run_id=14 ORDER BY match_id")
for r in cur.fetchall():
    print(f"#{r['match_id']} {r['home']} vs {r['away']} | 方向:{r['direction']} | {r['actual_score']} | 半全场:{r['half_full']} | {'Y' if r['hit'] else 'N'}")
cur.execute("SELECT total_matches, hit_count FROM runs WHERE id=14")
r = cur.fetchone()
print(f"\n汇总: {r['total_matches']}场 {r['hit_count']}中")
conn.close()
