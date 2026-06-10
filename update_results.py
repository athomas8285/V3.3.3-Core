import sqlite3, json
conn = sqlite3.connect(r"C:\Users\gjj\Desktop\v333\framework.db")
cur = conn.cursor()

# Update matches for run_id=14 (今日扫盘 2026-06-05)
updates = [
    ("201", "1-2", "负负", 0),  # 新加坡 1-2 中国
    ("202", "2-2", "平平", 0),  # 斯洛伐克 2-2 黑山
    ("203", "2-1", "胜胜", 1),  # 匈牙利 2-1 芬兰
    ("204", "1-1", "胜平", 1),  # 加拿大 1-1 爱尔兰
]

for mid, score, hf, hit in updates:
    cur.execute("""
        UPDATE matches 
        SET actual_score=?, half_full=?, half_time_score=?, hit=?, result_updated_at=datetime('now','localtime')
        WHERE run_id=14 AND match_id=?
    """, (score, hf, hf.split("-")[0] if "-" in hf else hf, hit, mid))
    print(f"#{mid}: score={score} hf={hf} hit={hit}")

# Update run_id=14 stats
cur.execute("UPDATE runs SET total_matches=4, hit_count=2 WHERE id=14")
print("run_id=14: total=4, hit=2")

conn.commit()
conn.close()
print("Done")
