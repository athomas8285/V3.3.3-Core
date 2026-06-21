import json

with open("D:\\V3.3.3-Core\\data\\match_info.json", "r", encoding="utf-8") as f:
    mi = json.load(f)

updated = 0
for m in mi.get("matches", []):
    mid = m["id"]
    if mid in ("周六033", "周六034", "周六035", "周六036"):
        dir_val = m.get("direction", "")
        score = m.get("actual_score", "")
        handicap = int(m.get("jc_handicap", 0) or 0)
        if score and ":" in score:
            hg, ag = int(score.split(":")[0]), int(score.split(":")[1])
            if dir_val == "胜": hit = hg > ag
            elif dir_val == "负": hit = hg < ag
            elif dir_val == "平": hit = hg == ag
            elif dir_val == "让胜": hit = (hg + handicap) > ag
            elif dir_val == "让负": hit = (hg + handicap) < ag
            elif dir_val == "让平": hit = (hg + handicap) == ag
            else: hit = None
            if hit is not None:
                m["hit"] = hit
                updated += 1
                print(f"  {mid}: {dir_val} {score} hc={handicap} -> HIT" if hit else f"  {mid}: {dir_val} {score} hc={handicap} -> MISS")

if updated:
    with open("D:\\V3.3.3-Core\\data\\match_info.json", "w", encoding="utf-8") as f:
        json.dump(mi, f, ensure_ascii=False, indent=2)
    print(f"\nUpdated {updated}")
