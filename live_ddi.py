"""live_ddi.py - V3.3.3-Core 临场DDI重校引擎
   输入新的SP赔率 → 重新计算DDI/贴合度/评级
   支持单场或全量重校"""

import json, os, copy, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# 导入现有计算函数
sys.path.insert(0, BASE_DIR)
from ddi import calc_market_prob, calc_ddi, apply_calibration, apply_away_cold_treatment
from fit_score import calc_fit_score, score_path_consistency, score_movement_match, score_data_confidence
from fit_score import score_injury_reliability, score_motivation_clarity, score_handicap_deviation
from fit_score import score_event_adaptability, apply_veto_rules, MAX_SCORE, NORMALIZE
from rating import determine_direction, check_wind_control, classify_scenario, determine_rating, get_rating_label
from config import FIT_SCORE_THRESHOLD_MELTDOWN


def load_current():
    """加载当前所有数据"""
    def load_json(name):
        path = os.path.join(DATA_DIR, name)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    return {
        "info": {m["id"]: m for m in load_json("match_info.json")["matches"]},
        "mc": {m["id"]: m for m in load_json("monte_carlo_result.json")["matches"]},
        "ddi": {m["id"]: m for m in load_json("ddi_result.json")["matches"]},
        "fit": {m["id"]: m for m in load_json("fit_score_result.json")["matches"]},
        "rating": {m["id"]: m for m in load_json("rating_result.json")["matches"]},
        "ai": {m["id"]: m for m in load_json("ai_judgment.json")["matches"]},
    }


def recalibrate(mid, new_sp_home, new_sp_draw, new_sp_away, 
                starting_lineup_confirmed=None, data=None):
    """对单场比赛进行临场重校"""
    if data is None:
        data = load_current()
    
    info = copy.deepcopy(data["info"].get(mid))
    mc = copy.deepcopy(data["mc"].get(mid))
    ai = copy.deepcopy(data["ai"].get(mid))
    old_ddi = data["ddi"].get(mid, {})
    old_fit = data["fit"].get(mid, {}).get("fit_score", {})
    old_rating = data["rating"].get(mid, {})
    
    if not all([info, mc, ai]):
        return {"error": f"比赛{mid}数据不完整"}
    
    before = {
        "sp": {"home": info["sp_home"], "draw": info["sp_draw"], "away": info["sp_away"]},
        "ddi": old_ddi.get("ddi", {}),
        "fit_score": old_fit.get("final_total", 0),
        "fit_details": old_fit.get("details", {}),
        "rating": old_rating.get("rating", ""),
        "direction": old_rating.get("direction", ""),
    }
    
    # Step 1: 用新赔率计算市场概率
    p_market = calc_market_prob(new_sp_home, new_sp_draw, new_sp_away)
    p_physical = mc["physical"]
    
    # Step 2: 计算新DDI
    ddi = calc_ddi(p_physical, p_market)
    calibrated = apply_calibration(p_physical, ddi)
    
    # Step 3: 赔率动量修正（用新SP作为当前SP）
    info["sp_home"] = new_sp_home
    info["sp_draw"] = new_sp_draw  
    info["sp_away"] = new_sp_away
    
    from ddi import apply_odds_momentum_correction
    calibrated = apply_odds_momentum_correction(calibrated, info)
    
    # Step 4: 客场冷处理
    predicted_direction = info.get("predicted_direction", "home")
    calibrated = apply_away_cold_treatment(
        calibrated, predicted_direction, 
        info.get("match_type", ""), info.get("is_home_life_death", False)
    )
    
    # Step 5: 重新计算 fit_score
    new_ddi_result = {
        "p_physical": p_physical,
        "p_market": {k: round(v, 4) for k, v in p_market.items()},
        "ddi": {k: round(v, 4) for k, v in ddi.items()},
        "calibrated": {k: round(v, 4) for k, v in calibrated.items()},
        "protection_triggered": False,
        "sp_missing": False
    }
    
    new_fit = calc_fit_score(info, new_ddi_result, ai)
    
    # Step 6: 首发阵容修正
    lineup_bonus = 0
    if starting_lineup_confirmed is True:
        lineup_bonus = 0.5  # 阵容确认加分
        new_fit["final_total"] = min(new_fit["final_total"] + lineup_bonus, 10.0)
    elif starting_lineup_confirmed is False:
        lineup_bonus = -1.0  # 核心缺阵扣分
        new_fit["final_total"] = max(new_fit["final_total"] + lineup_bonus, 0)
    
    # Step 7: 重新计算方向
    direction, direction_warning = determine_direction(
        p_physical, mc.get("jc_handicap_prob", {}), 
        info.get("lambda_diff", 0), new_sp_draw
    )
    
    # Step 8: 重新计算评级
    scenario_type, scenario_high_risk = classify_scenario(info, mc)
    downgrade = check_wind_control(info.get("asian_handicap", 0), info.get("lambda_diff", 0))
    
    internal_rating = determine_rating(
        new_fit["final_total"], downgrade, new_fit["meltdown"],
        info.get("match_type", ""), info.get("event", ""), scenario_high_risk
    )
    label = get_rating_label(internal_rating, new_fit["final_total"], scenario_type, direction_warning)
    
    # Step 9: 构建DDI变动摘要
    old_ddi_val = old_ddi.get("ddi", {})
    ddi_change = {}
    for k in ["home_win", "draw", "away_win"]:
        old = old_ddi_val.get(k, 0)
        new = ddi.get(k, 0)
        ddi_change[k] = {"old": round(old, 4), "new": round(new, 4), "delta": round(new - old, 4)}
    
    return {
        "match_id": mid,
        "home": info["home"],
        "away": info["away"],
        "event": info.get("event", ""),
        "time": info.get("time", ""),
        "before": before,
        "after": {
            "sp": {"home": new_sp_home, "draw": new_sp_draw, "away": new_sp_away},
            "p_market": {k: round(v, 4) for k, v in p_market.items()},
            "ddi": {k: round(v, 4) for k, v in ddi.items()},
            "ddi_change": ddi_change,
            "calibrated": {k: round(v, 4) for k, v in calibrated.items()},
            "fit_score": round(new_fit["final_total"], 2),
            "fit_details": new_fit["details"],
            "fit_level": new_fit["level"],
            "rating": label,
            "direction": direction,
            "direction_warning": direction_warning,
            "scenario_type": scenario_type,
            "lineup_bonus": lineup_bonus,
        },
    }


def recalibrate_all(odds_map, lineup_map=None):
    """全量重校 - odds_map: {mid: [sp_h, sp_d, sp_a]}"""
    data = load_current()
    results = []
    for mid, odds in odds_map.items():
        lineup_conf = (lineup_map or {}).get(mid)
        result = recalibrate(mid, *odds, starting_lineup_confirmed=lineup_conf, data=data)
        results.append(result)
    return results


if __name__ == "__main__":
    data = load_current()
    print("当前比赛列表:")
    for mid, info in sorted(data["info"].items()):
        old_rating = data["rating"].get(mid, {})
        print(f"  {mid}: {info['home']} vs {info['away']}  SP:{info['sp_home']}/{info['sp_draw']}/{info['sp_away']}  -> {old_rating.get('direction','')} ({old_rating.get('rating','')})")
    print()
    print("用法: POST /api/live/recalibrate  传入更新后的赔率")
