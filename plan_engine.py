# -*- coding: gbk -*-
"""plan_engine.py v2
策略：
- 单关：仅总进球、比分、半全场
- 复选/混合：作为串关腿，不做单独推荐
- 串关：跨比赛2串1为主，腿可任意搭配
"""
import json, math, itertools
from collections import defaultdict

def poisson_pmf(k, lam):
    if lam <= 0: return 0.0
    return (lam ** k) * math.exp(-lam) / math.factorial(k)

def compound_odds(odds_list):
    inv = sum(1.0 / o for o in odds_list if o > 0)
    return 1.0 / inv if inv > 0 else 0

def avg_score(items):
    return sum(x["score"] for x in items) / len(items)

def _make_dir():
    return "D:\\V3.3.3-Core\\data"

def load_today_data():
    base = _make_dir()
    with open(base + "\\match_info.json", "r", encoding="utf-8") as f:
        info = json.load(f)["matches"]
    with open(base + "\\monte_carlo_result.json", "r", encoding="utf-8") as f:
        mc = json.load(f)["matches"]
    with open(base + "\\rating_result.json", "r", encoding="utf-8") as f:
        rating = json.load(f)["matches"]
    return {m["id"]: m for m in info}, {m["id"]: m for m in mc}, {m["id"]: m for m in rating}

def generate_all_options(info_map, mc_map, rating_map):
    """生成所有选项（任何赔率），返回列表"""
    options = []
    for mid, info in info_map.items():
        if mid not in mc_map or mid not in rating_map: continue
        rdata = rating_map[mid]
        if rdata.get("meltdown"): continue
        fs = rdata.get("fit_score", 0)
        if fs < 6.0: continue
        match_label = info["home"] + " vs " + info["away"]
        direction = rdata.get("direction", "")

        def add(tp, opt, odds, prob):
            if odds <= 0 or prob <= 0: return
            edge = prob - 1.0 / odds
            score = round(prob * fs / 10.0 * (1.0 + edge), 4)
            options.append({"match_id":mid,"match":match_label,"type":tp,"option":opt,
                            "odds":odds,"model_prob":round(prob,4),"fit_score":fs,
                            "edge":round(edge,4),"score":score,"direction":direction})

        phys = mc_map[mid].get("physical",{})
        sp_w = info.get("jc_sp_win") or info.get("sp_home") or 0
        sp_d = info.get("jc_sp_draw") or info.get("sp_draw") or 0
        sp_l = info.get("jc_sp_lose") or info.get("sp_away") or 0
        for opt, odds, prob in [("主胜",sp_w,phys.get("home_win",0)),
                                ("平局",sp_d,phys.get("draw",0)),
                                ("客胜",sp_l,phys.get("away_win",0))]:
            add("胜平负", opt, odds, prob)

        hcp = mc_map[mid].get("jc_handicap_prob",{})
        hhad_w = info.get("jc_hhad_win",0); hhad_d = info.get("jc_hhad_draw",0); hhad_l = info.get("jc_hhad_lose",0)
        hc = info.get("jc_handicap", mc_map[mid].get("jc_handicap",0))
        hc_label = ("让"+str(hc)) if hc > 0 else ("受让"+str(abs(hc))) if hc < 0 else "中立"
        for opt, odds, prob in [("让胜",hhad_w,hcp.get("rang_sheng",0)),
                                ("让平",hhad_d,hcp.get("rang_ping",0)),
                                ("让负",hhad_l,hcp.get("rang_fu",0))]:
            if odds > 1.0:
                add("让球胜平负("+hc_label+")", opt, odds, prob)

        lam_h = mc_map[mid].get("lambda_h_final",1.0)
        lam_a = mc_map[mid].get("lambda_a_final",1.0)
        lam_t = lam_h + lam_a

        ttg = info.get("ttg_odds",{})
        if ttg:
            for k, v in ttg.items():
                try: g = int(k.lstrip("s"))
                except: continue
                p = poisson_pmf(g, lam_t)
                add("总进球数", (str(g)+"球" if g<7 else "7+球"), v, p)

        crs = info.get("crs_odds",{})
        if crs:
            for k, v in crs.items():
                if k.startswith("s") and "s" in k[1:]:
                    part = k[1:]
                    if part.count("s") == 1:
                        halves = part.split("s")
                        if halves[0].isdigit() and halves[1].isdigit():
                            hg, ag = int(halves[0]), int(halves[1])
                            p = poisson_pmf(hg, lam_h) * poisson_pmf(ag, lam_a)
                            add("比分", str(hg)+"-"+str(ag), v, p)

        hafu = info.get("hafu_odds",{})
        if hafu:
            hf_map = {"hh":"胜胜","hd":"胜平","ha":"胜负",
                      "dh":"平胜","dd":"平平","da":"平负",
                      "ah":"负胜","ad":"负平","aa":"负负"}
            for k, v in hafu.items():
                p_market = 1.0 / v if v > 1 else 0
                add("半全场", hf_map.get(k, k), v, p_market)

    return options

def filter_singles(options, min_odds, max_odds):
    """单关：仅非SP玩法，赔率在范围内"""
    non_sp = {"总进球数","比分","半全场"}
    ok = [o for o in options if o["type"] in non_sp and min_odds <= o["odds"] <= max_odds and o["score"] > 0]
    ok.sort(key=lambda x: -x["score"])
    return ok

def build_leg_pool(options):
    """构建所有可用腿池"""
    # --- 单选项腿 (所有玩法, 任何赔率) ---
    single_legs = []
    seen_ids = set()
    for o in options:
        if o["score"] <= 0 or o["odds"] < 1.01: continue
        key = (o["match_id"], o["type"], o["option"])
        if key in seen_ids: continue
        seen_ids.add(key)
        # EV 过滤: 仅对低赔腿(odds<1.20)要求正期望值,防止凑单式硬塞不稳胆码
        if o["odds"] < 1.20:
            ev = o["odds"] * o["model_prob"]
            if ev < 1.03: continue
        single_legs.append({
            "id": o["match_id"], "match": o["match"],
            "desc": o["type"]+" "+o["option"],
            "odds": o["odds"], "score": o["score"]
        })

    # --- 复选腿 (同比赛同玩法2-3个打包) ---
    groups = defaultdict(list)
    for o in options:
        if o["score"] > 0:
            groups[(o["match_id"], o["type"])].append(o)
    compound_legs = []
    seen = set()
    for key, items in groups.items():
        if len(items) < 2: continue
        for k in (2, 3):
            for combo in itertools.combinations(items, k):
                vodds = compound_odds([o["odds"] for o in combo])
                if vodds < 1.10: continue  # 赔率<1.1的组合受庄家抽水侵蚀严重,跳过
                labels = " + ".join(o["option"] for o in combo)
                cid = key[0] + "|" + key[1] + "|" + labels
                if cid in seen: continue
                seen.add(cid)
                # 复选打包 score 用概率之和重新计算, 而非子选项 score 的均值
                comp_prob = sum(o["model_prob"] for o in combo)
                comp_odds_val = compound_odds([o["odds"] for o in combo])
                if comp_odds_val <= 0: continue
                comp_edge = comp_prob - 1.0 / comp_odds_val
                comp_fs = combo[0]["fit_score"]
                comp_score = comp_prob * (comp_fs / 10.0) * (1.0 + comp_edge)
                if comp_odds_val < 1.10: continue  # 二次保险
                compound_legs.append({
                        "id": key[0], "match": combo[0]["match"],
                        "desc": "["+key[1]+"] "+labels,
                        "odds": round(comp_odds_val, 2),
                        "score": round(comp_score, 4)
                    })
    # 每场比赛取最优3个复选
    compound_legs.sort(key=lambda x: -x["score"])
    compound_top = []
    mid_groups = defaultdict(list)
    for cl in compound_legs:
        mid_groups[cl["id"]].append(cl)
    for mid, items in mid_groups.items():
        compound_top.extend(items[:3])

    # --- 混合腿 (同比赛不同玩法) ---
    match_items = defaultdict(list)
    for o in options:
        if o["score"] > 0:
            match_items[o["match_id"]].append(o)
    mix_legs = []
    seen2 = set()
    for mid, items in match_items.items():
        mn = items[0]["match"]
        for a, b in itertools.combinations(items, 2):
            if a["type"] == b["type"]: continue
            prod = round(a["odds"] * b["odds"], 2)
            d = a["type"]+" "+a["option"]+"@"+str(a["odds"])+" × "+b["type"]+" "+b["option"]+"@"+str(b["odds"])
            mid_key = mid + "|" + d
            if mid_key in seen2: continue
            seen2.add(mid_key)
            mix_legs.append({
                "id": mid, "match": mn,
                "desc": d, "odds": prod,
                "score": round((a["score"]+b["score"])/2, 4)
            })
    mix_legs.sort(key=lambda x: -x["score"])
    mix_top = mix_legs[:8]

    # --- 合并去重 ---
    all_legs = single_legs + compound_top + mix_top
    seen3 = set()
    final_legs = []
    for l in all_legs:
        k = (l["id"], l["desc"])
        if k not in seen3:
            seen3.add(k)
            final_legs.append(l)
    return final_legs

def generate_combos(legs, min_odds, max_odds, top_n=10):
    """跨比赛2串1 + 3串1"""
    combos_2 = []
    for a, b in itertools.combinations(legs, 2):
        if a["id"] == b["id"]: continue
        prod = round(a["odds"] * b["odds"], 2)
        if min_odds <= prod <= max_odds:
            combos_2.append({
                "legs": [{"desc":a["desc"],"odds":a["odds"],"match":a["match"]},
                         {"desc":b["desc"],"odds":b["odds"],"match":b["match"]}],
                "combined_odds": prod,
                "avg_score": round((a["score"]+b["score"])/2, 4)
            })
    combos_2.sort(key=lambda x: -x["avg_score"])

    combos_3 = []
    for a, b, c in itertools.combinations(legs, 3):
        ids = {a["id"], b["id"], c["id"]}
        if len(ids) != 3: continue
        prod = round(a["odds"] * b["odds"] * c["odds"], 2)
        if min_odds <= prod <= max_odds:
            combos_3.append({
                "legs": [{"desc":a["desc"],"odds":a["odds"],"match":a["match"]},
                         {"desc":b["desc"],"odds":b["odds"],"match":b["match"]},
                         {"desc":c["desc"],"odds":c["odds"],"match":c["match"]}],
                "combined_odds": prod,
                "avg_score": round((a["score"]+b["score"]+c["score"])/3, 4)
            })
    combos_3.sort(key=lambda x: -x["avg_score"])

    return combos_2[:top_n], combos_3[:top_n]

def recommend_plan(all_options, min_odds=2.0, max_odds=3.0, top_n=10):
    """总入口：单关 + 串关"""
    singles = filter_singles(all_options, min_odds, max_odds)
    legs = build_leg_pool(all_options)
    combos_2, combos_3 = generate_combos(legs, min_odds, max_odds, top_n)
    return singles[:top_n], combos_2, combos_3

if __name__ == "__main__":
    im, mm, rm = load_today_data()
    print("加载 " + str(len(im)) + " 场比赛")
    opts = generate_all_options(im, mm, rm)
    print("生成 " + str(len(opts)) + " 个选项")
    print()
    for lo, hi, label in [(2.0, 3.0, "2.0计划"), (3.0, 4.0, "3.0计划")]:
        singles, c2, c3 = recommend_plan(opts, lo, hi)
        print("=" * 60)
        print("  " + label)
        print("=" * 60)
        print("  单关 (" + str(len(singles)) + "个):")
        for s in singles:
            print("    [" + s["match_id"] + "] " + s["match"] + " | " + s["type"] + " " + s["option"] + " @ " + str(s["odds"]) + " score=" + str(s["score"]))
        print("  跨比赛2串1 (" + str(len(c2)) + "个):")
        for m in c2:
            d = " × ".join(l["desc"] + "@" + str(l["odds"]) for l in m["legs"])
            print("    " + d + " = " + str(m["combined_odds"]) + " score=" + str(m["avg_score"]))
        print("  跨比赛3串1 (" + str(len(c3)) + "个):")
        for m in c3:
            d = " × ".join(l["desc"] + "@" + str(l["odds"]) for l in m["legs"])
            print("    " + d + " = " + str(m["combined_odds"]) + " score=" + str(m["avg_score"]))

