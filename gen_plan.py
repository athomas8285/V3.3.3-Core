#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""

gen_plan.py — 精选计划单生成器

V3.3.3-Core 计划模块



功能：

- 从 match_info.json / rating_result.json / monte_carlo_result.json 读取比赛数据
# - 为每场比赛生成方向、总进球、半全场 三条腿（比分单腿已移除，保留打包）
# - 复选打包腿：总进球(0/1,2/3,3/4球)、半全场(主不败/客不败)、比分(主小胜/客小胜)、方向让球盘(让胜/平,让平/负)

- 组 2串1 方案，按 2.0/3.0 计划分档

- 输出 plan_data.json（给前端用）



用法：

    python gen_plan.py

    python gen_plan.py --prefix 周日     # 只处理周日开头的比赛

    python gen_plan.py --ids 周日037 周日038  # 只处理指定比赛

"""



import json, math, os, sys, itertools



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")





def load_json(path):

    with open(path, "r", encoding="utf-8") as f:

        return json.load(f)





def poisson(lmbda, k):

    if lmbda <= 0:

        return 0

    return (lmbda ** k) * math.exp(-lmbda) / math.factorial(k)





def total_goal_prob(lh, la, t):

    return sum(poisson(lh, k) * poisson(la, t - k) for k in range(t + 1))





# 映射表

HAFU_MAP = {

    "hh": "胜胜", "hd": "胜平", "ha": "胜负",

    "dh": "平胜", "dd": "平平", "da": "平负",

    "ah": "负胜", "ad": "负平", "aa": "负负"

}

SCORE_LABELS = {

    "s01s00": "1-0", "s02s00": "2-0", "s02s01": "2-1",

    "s03s00": "3-0", "s03s01": "3-1", "s03s02": "3-2",

    "s00s01": "0-1", "s00s02": "0-2", "s01s02": "1-2",

    "s00s03": "0-3", "s01s03": "1-3", "s02s03": "2-3",

    "s00s00": "0-0", "s01s01": "1-1", "s02s02": "2-2"

}





def generate_plan(output_dir=None, match_filter=None):

    """

    生成精选计划单数据

    match_filter: None=全部, "周日"=前缀匹配, ["周日037","周日038"]=指定列表

    """

    info_data = load_json(os.path.join(DATA_DIR, "match_info.json"))

    rating_data = load_json(os.path.join(DATA_DIR, "rating_result.json"))

    mc_data = load_json(os.path.join(DATA_DIR, "monte_carlo_result.json"))



    info_map = {m["id"]: m for m in info_data["matches"]}

    rating_map = {m["id"]: m for m in rating_data["matches"]}

    mc_map = {m["id"]: m for m in mc_data["matches"]}



    legs = []

    match_labels = {}



    def add_leg(mid, match, typ, opt, odds, mp, fit, rating, packed=False, sub_opts=None):

        if odds <= 1.0 or mp <= 0:

            return

        score = mp * (fit / 10.0)

        if score > 0:

            l = {"mid": mid, "match": match, "type": typ, "option": opt,

                 "odds": round(odds, 2), "mp": round(mp, 4),

                 "score": round(score, 4), "fit": round(fit, 1), "rating": rating}

            if packed:

                l["packed"] = True

                l["sub_options"] = sub_opts

            legs.append(l)



    for mid, info in info_map.items():

        # 过滤器

        if match_filter is not None:

            if isinstance(match_filter, str):

                if not mid.startswith(match_filter):

                    continue

            elif isinstance(match_filter, (list, tuple)):

                if mid not in match_filter:

                    continue



        if mid not in mc_map or mid not in rating_map:

            continue

        rat = rating_map[mid]

        mc = mc_map[mid]

        if rat.get("meltdown"):

            continue

        direction = rat.get("direction", "")

        if not direction:

            continue



        fit = rat.get("fit_score", 0) or 0

        rating_val = rat.get("rating", "")

        phys = mc.get("physical", {})

        lh = mc.get("lambda_h_final", 1.0)

        la = mc.get("lambda_a_final", 1.0)

        home = info.get("home", "")

        away = info.get("away", "")

        match_labels[mid] = f"{home} vs {away}"

        mstr = f"{home} vs {away}"



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



        # ---- 单腿 ----

        # 方向

        if has_sp and direction:

            if direction in ("胜", "home") and sp_h:

                add_leg(mid, mstr, "方向", "主胜", float(sp_h), phys.get("home_win", 0), fit, rating_val)

            elif direction in ("负", "away") and sp_a:

                add_leg(mid, mstr, "方向", "客胜", float(sp_a), phys.get("away_win", 0), fit, rating_val)

            elif direction in ("平", "draw") and sp_d:

                add_leg(mid, mstr, "方向", "平局", float(sp_d), phys.get("draw", 0), fit, rating_val)

            elif direction == "让胜" and hh_w:

                add_leg(mid, mstr, "方向", "让胜", float(hh_w), mc.get("jc_handicap_prob", {}).get("rang_sheng", 0), fit, rating_val)

            elif direction == "让负" and hh_l:

                add_leg(mid, mstr, "方向", "让负", float(hh_l), mc.get("jc_handicap_prob", {}).get("rang_fu", 0), fit, rating_val)

        elif not has_sp and direction:

            if direction == "胜" and hh_w:

                add_leg(mid, mstr, "方向", f"让胜({hcp})", float(hh_w), mc.get("jc_handicap_prob", {}).get("rang_sheng", 0), fit, rating_val)

            elif direction == "负" and hh_l:

                add_leg(mid, mstr, "方向", f"让负(+{abs(hcp)})", float(hh_l), mc.get("jc_handicap_prob", {}).get("rang_fu", 0), fit, rating_val)



        # 总进球

        tg_legs = []

        if ttg:

            for g in range(8):

                k = f"s{g}"

                if k in ttg:

                    od = float(ttg[k])

                    if 2.0 <= od <= 10.0:

                        mp = total_goal_prob(lh, la, g)

                        add_leg(mid, mstr, "总进球", f"{g}球", od, mp, fit, rating_val)

                        tg_legs.append({"opt": f"{g}球", "odds": od, "mp": mp, "score": mp * (fit / 10.0)})



        # 半全场

        hf_legs = []

        if hafu:

            for k, lbl in HAFU_MAP.items():

                if k in hafu:

                    od = float(hafu[k])

                    if 2.0 <= od <= 4.0:

                        add_leg(mid, mstr, "半全场", lbl, od, 1.0 / od, fit, rating_val)

                        hf_legs.append({"opt": lbl, "odds": od, "mp": 1.0 / od, "score": (1.0 / od) * (fit / 10.0)})



        # 比分

        cs_legs = []

        if crs:

            for k, lbl in SCORE_LABELS.items():

                if k in crs:

                    od = float(crs[k])

                    if 2.0 <= od <= 10.0:

                        parts = lbl.split("-")

                        hg, ag = int(parts[0]), int(parts[1])

                        mp = poisson(lh, hg) * poisson(la, ag)

                        # 比分单腿已移除（保留cs_legs用于打包）

                        cs_legs.append({"opt": lbl, "odds": od, "mp": mp, "score": mp * (fit / 10.0)})



        # ===== 打包腿 =====

        # 1. 总进球打包: 所有相邻球数对(0/1 ~ 6/7)

        for g in range(7):  # 所有相邻球数对: 0/1, 1/2, ..., 6/7
            pack_size = (g, g + 1)

            popts = [l for l in tg_legs if l["opt"] in [f"{g}球" for g in pack_size]]

            if len(popts) == 2:

                p_odds = 1.0 / sum(1.0 / l["odds"] for l in popts)

                p_mp = sum(l["mp"] for l in popts)

                p_score = (popts[0]["score"] + popts[1]["score"]) / 2.0

                add_leg(mid, mstr, "总进球打包", f"{pack_size[0]}/{pack_size[1]}球", p_odds, p_mp, fit, rating_val,

                        packed=True, sub_opts=[l["opt"] for l in popts])



        # 2. 半全场打包: 主不败(胜胜+平胜), 客不败(负负+平负)

        for opts_lbl, pack_name in [(["胜胜", "平胜"], "主不败"), (["负负", "平负"], "客不败")]:

            popts = [l for l in hf_legs if l["opt"] in opts_lbl]

            if len(popts) >= 2:

                p_odds = 1.0 / sum(1.0 / l["odds"] for l in popts)

                p_mp = sum(l["mp"] for l in popts)

                p_score = sum(l["score"] for l in popts) / len(popts)

                add_leg(mid, mstr, "半全场打包", pack_name, p_odds, p_mp, fit, rating_val,

                        packed=True, sub_opts=[l["opt"] for l in popts])



        # 3. 比分打包: 主小胜(1-0+2-0), 客小胜(0-1+0-2)

        for opts_lbl, pack_name in [(["1-0", "2-0"], "主小胜"), (["0-1", "0-2"], "客小胜")]:

            popts = [l for l in cs_legs if l["opt"] in opts_lbl]

            if len(popts) >= 2:

                p_odds = 1.0 / sum(1.0 / l["odds"] for l in popts)

                p_mp = sum(l["mp"] for l in popts)

                p_score = sum(l["score"] for l in popts) / len(popts)

                add_leg(mid, mstr, "比分打包", pack_name, p_odds, p_mp, fit, rating_val,

                        packed=True, sub_opts=[l["opt"] for l in popts])



        # 4. 方向打包(让球盘): 让胜/平, 让平/负

        if hh_w and hh_d and hh_l:

            hcp_prob = mc.get("jc_handicap_prob", {})

            for odds_dict, pack_name in [

                ({"让胜": float(hh_w), "让平": float(hh_d)}, "让胜/平"),

                ({"让平": float(hh_d), "让负": float(hh_l)}, "让平/负"),

            ]:

                opts_list = []

                for opt_name, od_f in odds_dict.items():

                    if od_f > 1.0:

                        mp_key = {"让胜": "rang_sheng", "让平": "rang_ping", "让负": "rang_fu"}.get(opt_name)

                        mp_val = hcp_prob.get(mp_key, 0) if mp_key else 0

                        sc = mp_val * (fit / 10.0)

                        opts_list.append({"opt": opt_name, "odds": od_f, "mp": mp_val, "score": sc})

                if len(opts_list) >= 2:

                    p_odds = 1.0 / sum(1.0 / l["odds"] for l in opts_list)

                    p_mp = sum(l["mp"] for l in opts_list)

                    p_score = sum(l["score"] for l in opts_list) / len(opts_list)

                    add_leg(mid, mstr, "方向打包", pack_name, p_odds, p_mp, fit, rating_val,

                            packed=True, sub_opts=[l["opt"] for l in opts_list])



    legs.sort(key=lambda x: x["score"], reverse=True)



    # 组2串1

    combos = []

    for i in range(len(legs)):

        for j in range(i + 1, len(legs)):

            l1, l2 = legs[i], legs[j]

            if l1["mid"] == l2["mid"]:

                continue

            co = l1["odds"] * l2["odds"]

            if co < 2.0 or co > 4.0:

                continue

            # 方向打包权重提升1.3x（历史命中率60%）
            w1 = 1.3 if l1.get("type") == "方向打包" else 1.0
            w2 = 1.3 if l2.get("type") == "方向打包" else 1.0
            avg = (l1["score"] * w1 + l2["score"] * w2) / 2.0

            combos.append({"l1": l1, "l2": l2, "odds": round(co, 2), "score": round(avg, 4)})



    combos.sort(key=lambda x: x["score"], reverse=True)

    plan_2 = [c for c in combos if 2.0 <= c["odds"] < 3.0]

    plan_3 = [c for c in combos if 3.0 <= c["odds"] <= 4.0]



    data = {

        "date": "2026-06-22",

        "matches": match_labels,

        "total_matches": len(match_labels),

        "total_legs": len(legs),

        "plan_2_count": len(plan_2),

        "plan_3_count": len(plan_3),

        "top": plan_2[0] if plan_2 else (plan_3[0] if plan_3 else None),

        "plan_2": plan_2[:10],

        "plan_3": plan_3[:10],

        "legs": legs

    }



    single_cnt = sum(1 for l in legs if not l.get("packed"))

    packed_cnt = sum(1 for l in legs if l.get("packed"))

    print(f"单腿: {single_cnt}, 打包腿: {packed_cnt}, 总: {len(legs)}")

    print(f"2.0方案: {len(plan_2)}, 3.0方案: {len(plan_3)}")

    if data["top"]:

        t = data["top"]

        print(f"最推荐: {t['l1']['option']}@{t['l1']['odds']} x {t['l2']['option']}@{t['l2']['odds']} = {t['odds']}")

        print(f"  L1: [{t['l1']['type']}] {t['l1']['match']}")

        print(f"  L2: [{t['l2']['type']}] {t['l2']['match']}")



    if output_dir is None:

        output_dir = DATA_DIR

    os.makedirs(output_dir, exist_ok=True)

    out_path = os.path.join(output_dir, "plan_data.json")

    with open(out_path, "w", encoding="utf-8") as f:

        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n已写入: {out_path}")

    return data





def generate_all_days(output_dir=None):

    """周四周四周四周四周四周四周四周四周四?"""

    if output_dir is None:

        output_dir = DATA_DIR

    os.makedirs(output_dir, exist_ok=True)

    prefixes = ["周四", "周四", "周四", "周四", "周四", "周四", "周四"]

    day_labels = {"周四":"6/12", "周四":"6/13", "周四":"6/14",

                  "周四":"6/15", "周四":"6/16", "周四":"6/17", "周四":"6/18"}

    results = {}

    for prefix in prefixes:

        data = generate_plan(match_filter=prefix, output_dir=output_dir)

        results[prefix] = {

            "label": day_labels.get(prefix, prefix),

            "matches": len(data.get("matches", {})),

            "legs": data.get("total_legs", 0),

            "plan_2": data.get("plan_2_count", 0),

            "plan_3": data.get("plan_3_count", 0),

            "top": data.get("top")

        }

        label = day_labels.get(prefix, prefix)

        print(f"  {label} ({prefix}): {results[prefix]['matches']}? {results[prefix]['legs']}周四")

    return results



if __name__ == "__main__":

    filter_arg = None

    if len(sys.argv) > 1:

        if sys.argv[1] == "--prefix" and len(sys.argv) > 2:

            filter_arg = sys.argv[2]

        elif sys.argv[1] == "--ids" and len(sys.argv) > 2:

            filter_arg = sys.argv[2:]

        elif sys.argv[1] == "--by-day":

            print("周四周四周四周四...")

            generate_all_days()

            sys.exit(0)

    generate_plan(match_filter=filter_arg)

