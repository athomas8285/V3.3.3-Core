import json, math, os

# Load data
mi = json.load(open("D:/V3.3.3-Core/data/match_info.json", "r", encoding="utf-8", errors="replace"))
info_map = {m["id"]: m for m in mi["matches"]}

# Also load history.csv for direction + rating
import csv
h = open("D:/V3.3.3-Core/history.csv", "r", encoding="utf-8-sig").read().replace("\r\n", "\n")
hr = list(csv.DictReader(h.split("\n")))
hist_map = {r["id"]: r for r in hr}

def poisson(lmbda, k):
    if lmbda <= 0: return 0
    return (lmbda ** k) * math.exp(-lmbda) / math.factorial(k)

def total_goal_prob(lh, la, t):
    return sum(poisson(lh, k) * poisson(la, t - k) for k in range(t + 1))

HAFU_MAP = {"hh":"胜胜","hd":"胜平","ha":"胜负","dh":"平胜","dd":"平平","da":"平负","ah":"负胜","ad":"负平","aa":"负负"}
SCORE_LABELS = {"s01s00":"1-0","s02s00":"2-0","s02s01":"2-1","s03s00":"3-0","s03s01":"3-1","s03s02":"3-2",
                "s00s01":"0-1","s00s02":"0-2","s01s02":"1-2","s00s03":"0-3","s01s03":"1-3","s02s03":"2-3",
                "s00s00":"0-0","s01s01":"1-1","s02s02":"2-2"}

results = []
for mid, info in info_map.items():
    hist = hist_map.get(mid)
    if not hist: continue
    
    actual_score = info.get("actual_score", "")
    if not actual_score or ":" not in str(actual_score):
        continue
    
    try:
        hg, ag = map(int, str(actual_score).split(":"))
    except:
        try:
            hg, ag = map(int, str(actual_score).split("-"))
        except:
            continue
    
    actual_total = hg + ag
    direction = hist.get("direction", "")
    fit_score = float(hist.get("fit_score", 0) or 0)
    rating_val = hist.get("rating", "")
    lh = float(hist.get("lambda_final_h", 1.0) or 1.0)
    la = float(hist.get("lambda_final_a", 1.0) or 1.0)
    sp_h = info.get("sp_home")
    sp_d = info.get("sp_draw")
    sp_a = info.get("sp_away")
    hh_w = info.get("jc_hhad_win")
    hh_d = info.get("jc_hhad_draw")
    hh_l = info.get("jc_hhad_lose")
    hcp = info.get("jc_handicap", 0)
    has_sp = sp_h is not None
    ttg = info.get("ttg_odds", {})
    hafu = info.get("hafu_odds", {})
    crs = info.get("crs_odds", {})
    
    legs = []
    
    # Direction leg
    if direction == "胜" and sp_h:
        hit = hg > ag
        legs.append({"type":"方向","opt":"主胜","odds":sp_h,"hit":hit,"packed":False})
    elif direction == "负" and sp_a:
        hit = hg < ag
        legs.append({"type":"方向","opt":"客胜","odds":sp_a,"hit":hit,"packed":False})
    elif direction == "平" and sp_d:
        hit = hg == ag
        legs.append({"type":"方向","opt":"平局","odds":sp_d,"hit":hit,"packed":False})
    elif direction == "让胜" and hh_w:
        jc_hcp = int(float(hist.get("jc_handicap", 0) or 0))
        hit = (hg - ag + (-jc_hcp)) > 0
        legs.append({"type":"方向","opt":"让胜","odds":hh_w,"hit":hit,"packed":False})
    elif direction == "让负" and hh_l:
        jc_hcp = int(float(hist.get("jc_handicap", 0) or 0))
        hit = (hg - ag + (-jc_hcp)) < 0
        legs.append({"type":"方向","opt":"让负","odds":hh_l,"hit":hit,"packed":False})
    
    # Total goals legs
    if ttg:
        for g in range(8):
            k = f"s{g}"
            if k in ttg:
                odds = float(ttg[k])
                if 2.0 <= odds <= 10.0:
                    hit = actual_total == g
                    legs.append({"type":"总进球","opt":f"{g}球","odds":odds,"hit":hit,"packed":False})
        # Packed: 2/3球, 3/4球
        for ps in [(2,3),(3,4)]:
            o1 = ttg.get(f"s{ps[0]}")
            o2 = ttg.get(f"s{ps[1]}")
            if o1 and o2:
                o1f, o2f = float(o1), float(o2)
                if 2.0 <= o1f <= 10.0 and 2.0 <= o2f <= 10.0:
                    p_odds = 1.0 / (1.0/o1f + 1.0/o2f)
                    hit = actual_total in ps
                    legs.append({"type":"总进球打包","opt":f"{ps[0]}/{ps[1]}球","odds":round(p_odds,2),"hit":hit,"packed":True})
    
    # Half-full legs
    hf_legs = []
    if hafu:
        for k, lbl in HAFU_MAP.items():
            if k in hafu:
                od = float(hafu[k])
                if 2.0 <= od <= 4.0:
                    hf_legs.append({"opt": lbl, "odds": od})
        half_full_actual = info.get("half_full", "")
        for l in hf_legs:
            hit = l["opt"] == half_full_actual
            legs.append({"type":"半全场","opt":l["opt"],"odds":l["odds"],"hit":hit,"packed":False})
        # Packed: 主不败(胜胜+平胜), 客不败(负负+平负)
        for opts_lbl, pack_name in [(["胜胜","平胜"],"主不败"),(["负负","平负"],"客不败")]:
            ol = [l for l in hf_legs if l["opt"] in opts_lbl]
            if len(ol) >= 2:
                p_odds = 1.0 / sum(1.0/l["odds"] for l in ol)
                hit = half_full_actual in opts_lbl
                legs.append({"type":"半全场打包","opt":pack_name,"odds":round(p_odds,2),"hit":hit,"packed":True})
    
    # Score legs
    cs_legs = []
    if crs:
        for k, lbl in SCORE_LABELS.items():
            if k in crs:
                od = float(crs[k])
                if 2.0 <= od <= 10.0:
                    cs_legs.append({"opt": lbl, "odds": od})
        for l in cs_legs:
            hit = l["opt"] == actual_score
            legs.append({"type":"比分","opt":l["opt"],"odds":l["odds"],"hit":hit,"packed":False})
        # Packed: 主小胜(1-0+2-0), 客小胜(0-1+0-2)
        for opts_lbl, pack_name in [(["1-0","2-0"],"主小胜"),(["0-1","0-2"],"客小胜")]:
            ol = [l for l in cs_legs if l["opt"] in opts_lbl]
            if len(ol) >= 2:
                p_odds = 1.0 / sum(1.0/l["odds"] for l in ol)
                hit = actual_score in opts_lbl
                legs.append({"type":"比分打包","opt":pack_name,"odds":round(p_odds,2),"hit":hit,"packed":True})
    
    # Direction packed (handicap): 让胜/平, 让平/负
    if hh_w and hh_d and hh_l:
        for odds_dict, pack_name in [
            ({"让胜":float(hh_w),"让平":float(hh_d)},"让胜/平"),
            ({"让平":float(hh_d),"让负":float(hh_l)},"让平/负")
        ]:
            ol = [{"opt":n,"odds":v} for n,v in odds_dict.items() if v>1.0]
            if len(ol) >= 2:
                p_odds = 1.0 / sum(1.0/l["odds"] for l in ol)
                jc_hcp = int(float(hist.get("jc_handicap", 0) or 0))
                jc_score = hg - ag + (-jc_hcp)
                if pack_name == "让胜/平":
                    hit = jc_score >= 0
                else:
                    hit = jc_score <= 0
                legs.append({"type":"方向打包","opt":pack_name,"odds":round(p_odds,2),"hit":hit,"packed":True})
    
    results.append({"id": mid, "score": f"{hg}-{ag}", "direction": direction, "fit": fit_score, "rating": rating_val, "legs": legs})

# Statistics
total_matches = len(results)
all_legs = []
for r in results:
    for l in r["legs"]:
        all_legs.append({**l, "mid": r["id"], "fit": r["fit"]})

print(f"\n{'='*70}")
print(f"  精选计划单验证报告（{total_matches}场已完赛）")
print(f"{'='*70}")

by_type = {}
for l in all_legs:
    t = l["type"]
    if t not in by_type: by_type[t] = {"total":0,"hit":0}
    by_type[t]["total"] += 1
    if l["hit"]: by_type[t]["hit"] += 1

print(f"\n{'腿部类型':<16}{'总数':>6}{'命中':>6}{'命中率':>8}")
print("  " + "-"*40)
for t in ["方向","总进球","总进球打包","半全场","半全场打包","比分","比分打包","方向打包"]:
    if t in by_type:
        d = by_type[t]
        rate = d["hit"]/d["total"]*100 if d["total"]>0 else 0
        print(f"  {t:<14}{d['total']:>6}{d['hit']:>6}{rate:>7.1f}%")

all_total = sum(d["total"] for d in by_type.values())
all_hit = sum(d["hit"] for d in by_type.values())
print(f"\n  综合: {all_hit}/{all_total} = {all_hit/all_total*100:.1f}%")

# 2串1 verification - build combos from legs
print(f"\n{'='*70}")
print(f"  2串1回测")
print(f"{'='*70}")
legs_list = []
for r in results:
    for l in r["legs"]:
        legs_list.append({"mid":r["id"],"type":l["type"],"opt":l["opt"],"odds":l["odds"],"hit":l["hit"],"fit":r["fit"]})

combo_total = 0
combo_hit = 0
combo_2_total = 0
combo_2_hit = 0
combo_3_total = 0
combo_3_hit = 0

for i in range(len(legs_list)):
    for j in range(i+1, len(legs_list)):
        l1, l2 = legs_list[i], legs_list[j]
        if l1["mid"] == l2["mid"]: continue
        co = l1["odds"] * l2["odds"]
        if co < 2.0 or co > 4.0: continue
        hit = l1["hit"] and l2["hit"]
        combo_total += 1
        if hit: combo_hit += 1
        if co < 3.0:
            combo_2_total += 1
            if hit: combo_2_hit += 1
        else:
            combo_3_total += 1
            if hit: combo_3_hit += 1

print(f"\n  总组合: {combo_total}")
print(f"  总命中: {combo_hit} ({combo_hit/combo_total*100:.1f}%)" if combo_total>0 else "  总命中: 0")
print(f"\n  2.0方案: {combo_2_total} -> 命中 {combo_2_hit} ({combo_2_hit/combo_2_total*100:.1f}%)" if combo_2_total>0 else "  2.0方案: 0")
print(f"  3.0方案: {combo_3_total} -> 命中 {combo_3_hit} ({combo_3_hit/combo_3_total*100:.1f}%)" if combo_3_total>0 else "  3.0方案: 0")

# Per match detail
print(f"\n{'='*70}")
print(f"  逐场详情")
print(f"{'='*70}")
for r in results:
    leg_str = " | ".join([f"{'H' if l['hit'] else '-'}{l['type']}:{l['opt']}@{l['odds']:.1f}" for l in r["legs"][:5]])
    if len(r["legs"]) > 5:
        leg_str += f" ...(+{len(r['legs'])-5})"
    print(f"  [{r['id']}] {r['score']} dir={r['direction']} fit={r['fit']} | {leg_str}")

print(f"\n{'='*70}")
print(f"  回测完成")