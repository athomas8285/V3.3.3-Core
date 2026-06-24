import re

# Read plan_周日.html and extract the DATA
html = open("D:/V3.3.3-Core/data/plan_周日.html", "r", encoding="utf-8", errors="replace").read()
m = re.search(r"var DATA = ({.*?});", html, re.DOTALL)
import json
data = json.loads(m.group(1))

# Actual results
results = {
    "周日037": {"score": "4-0", "hafu": "胜胜"},
    "周日038": {"score": "0-0", "hafu": "平平"},
    "周日039": {"score": "2-2", "hafu": "胜平"},
    "周日040": {"score": "1-3", "hafu": "胜负"},
}

# Build hit map for each leg
def leg_hit(leg, results):
    mid = leg["mid"]
    if mid not in results: return None
    r = results[mid]
    hg, ag = int(r["score"].split("-")[0]), int(r["score"].split("-")[1])
    typ = leg["type"]
    opt = leg["option"]
    
    # Get handicap from match_info
    # We know: 037 hcp=-2, 038 hcp=-1, 039 hcp=-1, 040 hcp=1
    hcp_map = {"周日037": -2, "周日038": -1, "周日039": -1, "周日040": 1}
    hcp = hcp_map.get(mid, 0)
    jc_score = hg - ag + (-hcp)
    
    if typ == "方向":
        if opt == "主胜": return hg > ag
        elif opt == "客胜": return hg < ag
        elif opt == "平局": return hg == ag
        elif "让胜" in opt: return jc_score > 0
        elif "让负" in opt: return jc_score < 0
    elif typ == "方向打包":
        if opt == "让胜/平": return jc_score >= 0
        elif opt == "让平/负": return jc_score <= 0
    elif typ == "总进球":
        g = int(opt[0])
        return hg + ag == g
    elif typ == "总进球打包":
        parts = opt.split("/")
        g1, g2 = int(parts[0]), int(parts[1].replace("球",""))
        act = hg + ag
        return act >= min(g1,g2) and act <= max(g1,g2)
    elif typ == "半全场":
        return opt == r["hafu"]
    elif typ == "半全场打包":
        if opt == "主不败": return r["hafu"] in ["胜胜","平胜"]
        elif opt == "客不败": return r["hafu"] in ["负负","平负"]
    elif typ == "比分":
        return opt == r["score"]
    elif typ == "比分打包":
        if opt == "主小胜": return r["score"] in ["1-0","2-0"]
        elif opt == "客小胜": return r["score"] in ["0-1","0-2"]
    return None

# Verify each leg
print("=== 涉及周日037-040的腿部验证 ===")
for i, leg in enumerate(data["legs"]):
    mid = leg["mid"]
    if mid not in results: continue
    hit = leg_hit(leg, results)
    hl = "HIT" if hit else "MISS" if hit is not None else "N/A"
    if hit is not None:
        print(f"  {i:>2}. [{mid}] {leg['type']:<8} {leg['option']:<12} @{leg['odds']:<5} {hl}")

# Verify combos
print(f"\n=== 2.0方案回测 ===")
hit_combos = []
miss_combos = []
for c in data.get("plan_2", []):
    m1, m2 = c["l1"]["mid"], c["l2"]["mid"]
    if m1 not in results and m2 not in results: continue
    h1 = leg_hit(c["l1"], results)
    h2 = leg_hit(c["l2"], results)
    if h1 is None: h1 = True  # Skip verification for non-037-040 matches
    if h2 is None: h2 = True
    if h1 is None and h2 is None: continue
    
    combo_hit = h1 and h2
    l = "HIT" if combo_hit else "MISS"
    if combo_hit: hit_combos.append(c)
    else: miss_combos.append(c)
    print(f"  {l}: {c['l1']['option']}@{c['l1']['odds']} ({m1}) x {c['l2']['option']}@{c['l2']['odds']} ({m2}) = {c['odds']}")

print(f"\n  命中: {len(hit_combos)}/{len(hit_combos)+len(miss_combos)}")

# Count combos where BOTH legs are from 037-040
print(f"\n=== 双腿都在周日037-040的方案 ===")
both_hit = 0
both_total = 0
for c in data.get("plan_2", []) + data.get("plan_3", []):
    m1, m2 = c["l1"]["mid"], c["l2"]["mid"]
    if m1 not in results or m2 not in results: continue
    h1 = leg_hit(c["l1"], results)
    h2 = leg_hit(c["l2"], results)
    ch = h1 and h2
    both_total += 1
    if ch: both_hit += 1
    print(f"  {'HIT' if ch else 'MISS'}: {c['l1']['option']}@{c['l1']['odds']} x {c['l2']['option']}@{c['l2']['odds']} = {c['odds']}")

print(f"\n  命中: {both_hit}/{both_total}")