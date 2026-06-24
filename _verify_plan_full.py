import json, os, csv, re

# Read raw bytes, extract data by regex to avoid encoding corruption
raw = open("D:/V3.3.3-Core/data/match_info.json", "rb").read()
id_list = re.findall(b'"id": "([^"]+)"', raw)
raw_scores = re.findall(b'"actual_score": "([^"]+)"', raw)
raw_dirs = re.findall(b'"direction": "([^"]+)"', raw)
raw_ratings = re.findall(b'"rating": "([^"]+)"', raw)
raw_fit = re.findall(b'"fit_score": ([0-9.]+)', raw)
raw_hafu = re.findall(b'"half_full": "([^"]+)"', raw)
raw_hcp = re.findall(b'"jc_handicap": (-?[0-9.]+)', raw)
raw_sp_h = re.findall(b'"sp_home": ([0-9.]+)', raw)
raw_sp_d = re.findall(b'"sp_draw": ([0-9.]+)', raw)
raw_sp_a = re.findall(b'"sp_away": ([0-9.]+)', raw)
raw_hh_w = re.findall(b'"jc_hhad_win": "?([0-9.]+)"?', raw)
raw_hh_d = re.findall(b'"jc_hhad_draw": "?([0-9.]+)"?', raw)
raw_hh_l = re.findall(b'"jc_hhad_lose": "?([0-9.]+)"?', raw)

# Check for ttg_odds presence
ttg_present = re.findall(b'"ttg_odds"', raw)
print(f"Matches: {len(id_list)}, scores: {len(raw_scores)}, directions: {len(raw_dirs)}")
print(f"Ratings: {len(raw_ratings)}, half_full: {len(raw_hafu)}, ttg_odds: {len(ttg_present)}")

# Build structured data
parsed = []
for i in range(len(id_list)):
    mid = id_list[i].decode("utf-8", errors="replace")
    score_b = raw_scores[i] if i < len(raw_scores) else b""
    score_str = score_b.decode("utf-8", errors="replace")
    has_score = ":" in score_str or "-" in score_str
    hg = ag = -1
    if has_score:
        parts = score_str.replace("-", ":").split(":")
        try: hg, ag = int(parts[0]), int(parts[1])
        except: pass
    
    # For matches without explicit actual_score field, check hist CSV
    # We'll check if score is valid
    
    dir_str = raw_dirs[i].decode("utf-8", errors="replace") if i < len(raw_dirs) else ""
    rating_str = raw_ratings[i].decode("utf-8", errors="replace") if i < len(raw_ratings) else ""
    fit_str = raw_fit[i].decode() + ".0" if i < len(raw_fit) else "0"
    fit_val = float(raw_fit[i].decode()) if i < len(raw_fit) else 0
    half_full_str = raw_hafu[i].decode("utf-8", errors="replace") if i < len(raw_hafu) else ""
    hcp_str = raw_hcp[i].decode() if i < len(raw_hcp) else "0"
    jc_hcp = int(float(hcp_str))
    
    # Check direction hit
    dir_correct = None
    if dir_str == "胜" and hg >= 0: dir_correct = hg > ag
    elif dir_str == "负" and hg >= 0: dir_correct = hg < ag
    elif dir_str == "平" and hg >= 0: dir_correct = hg == ag
    elif dir_str == "让胜" and hg >= 0: dir_correct = (hg - ag + (-jc_hcp)) > 0
    elif dir_str == "让负" and hg >= 0: dir_correct = (hg - ag + (-jc_hcp)) < 0
    
    parsed.append({
        "id": mid, "score": f"{hg}-{ag}" if hg >= 0 else "",
        "hg": hg, "ag": ag, "direction": dir_str, "rating": rating_str,
        "fit": round(fit_val, 1), "half_full": half_full_str,
        "jc_hcp": jc_hcp,
        "dir_correct": dir_correct,
        "hafu": raw_hafu[i].decode("utf-8", errors="replace") if i < len(raw_hafu) else ""
    })

# Direction statistics
scored = [p for p in parsed if p["hg"] >= 0]
dir_scored = [p for p in scored if p["dir_correct"] is not None]
dir_hit = sum(1 for p in dir_scored if p["dir_correct"])

print(f"\n{'='*70}")
print(f"  精选计划单方向回测（{len(scored)}场）")
print(f"{'='*70}")
print(f"  方向命中: {dir_hit}/{len(dir_scored)} = {dir_hit/len(dir_scored)*100:.1f}%")

# By rating tier
for tier in ["S", "A", "B", "C"]:
    tm = [p for p in dir_scored if p["rating"] == tier]
    if not tm: continue
    th = sum(1 for p in tm if p["dir_correct"])
    print(f"  {tier}级推荐: {th}/{len(tm)} = {th/len(tm)*100:.1f}%")

# Half-full check where available
hf_scored = [p for p in scored if p["half_full"] and p["half_full"] in ["胜胜","胜平","胜负","平胜","平平","平负","负胜","负平","负负"]]
print(f"\n  半全场有值: {len(hf_scored)}场")

# Detail table
print(f"\n{'='*70}")
print(f"  {'ID':<10} {'比分':<8} {'方向':<8} {'命?':<4} {'fit':<5} {'评级':<4}")
print(f"  {'-'*45}")
for p in scored:
    dot = ""
    if p["dir_correct"] is True: dot = "Y"
    elif p["dir_correct"] is False: dot = "N"
    else: dot = "?"
    print(f"  {p['id']:<10} {p['score']:<8} {p['direction']:<8} {dot:<4} {p['fit']:<5} {p['rating']:<4}")