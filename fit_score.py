# fit_score.py
# V3.3.3-Core-Rev1.13 Step 8: 贴合度评估（xG差拆分版）
# P0-P4: 置信度/样本量感知优化

import json, os
from config import FIT_SCORE_THRESHOLD_MELTDOWN, OPPONENT_PREDICTABILITY_MIN
from lambda_calc import _confidence_scale, detect_cross_tournament_xg, _data_confidence_multiplier

MAX_SCORE = 11.0
NORMALIZE = 10.0 / MAX_SCORE


def score_data_confidence(match_data):
    """
    P0/P3: 基于置信度等级的数据可靠性评分。
    替代旧的二元缺失检查，使用 h2h_confidence/xg_last3_confidence/
    xg_season_confidence/roster_confidence 字段。
    回退：若缺少置信度字段，使用旧的 _missing 字段做兼容。
    """
    CONF_MAP = {"api": 1.0, "calc": 0.7, "infer": 0.3}
    score = 1.5

    # Check if confidence fields exist (P0 data)
    has_conf_fields = any(k in match_data for k in
                          ["h2h_confidence", "xg_last3_confidence",
                           "xg_season_confidence", "roster_confidence"])

    if has_conf_fields:
        h2h_conf = _data_confidence_multiplier(match_data.get("h2h_confidence", "api"))
        xg_last3_conf = _data_confidence_multiplier(match_data.get("xg_last3_confidence", "calc"))
        xg_season_conf = _data_confidence_multiplier(match_data.get("xg_season_confidence", "api"))
        roster_conf = _data_confidence_multiplier(match_data.get("roster_confidence", "api"))

        avg_conf = (h2h_conf + xg_last3_conf + xg_season_conf + roster_conf) / 4.0
        score = 1.5 * avg_conf

        # Extra penalty when both xg data sources are weak
        if xg_season_conf < 0.5 and xg_last3_conf < 0.5:
            score *= 0.7

        # P1: Sample size penalty
        sample_penalty = _confidence_scale(
            match_data.get("xg_home_sample", 0),
            match_data.get("xg_away_sample", 0),
            match_data.get("xg_last3_home_sample", 0),
            match_data.get("xg_last3_away_sample", 0)
        )
        score *= sample_penalty

        # P2: Cross-tournament penalty
        cross_penalty, _ = detect_cross_tournament_xg(
            match_data.get("xg_home_source_events", ""),
            match_data.get("xg_away_source_events", "")
        )
        score *= cross_penalty
    else:
        # Fallback: binary missing flags (old behavior)
        if match_data.get("h2h_missing", False): score -= 0.15
        if match_data.get("xg_last3_missing", False): score -= 0.4
        if match_data.get("xg_season_missing", False): score -= 0.25
        if match_data.get("xg_season_missing", False) and match_data.get("away_xg_missing", False):
            score -= 0.25
        if match_data.get("xg_last3_missing", False) and match_data.get("roster_missing", False):
            score = min(score, 0.75)

    return max(0, score)


def score_injury_reliability(match_data):
    """
    P0: 使用置信度字段的伤病可靠性评分。
    仍保留旧的二进制检查作为回退。
    """
    score = 1.0

    if "injury_home_confidence" in match_data or "injury_away_confidence" in match_data:
        h_inj_conf = _data_confidence_multiplier(match_data.get("injury_home_confidence", "api"))
        a_inj_conf = _data_confidence_multiplier(match_data.get("injury_away_confidence", "api"))
        src_conf = _data_confidence_multiplier(match_data.get("injury_source_confidence", "calc"))
        avg_inj_conf = (h_inj_conf + a_inj_conf) / 2.0
        score = 1.0 * avg_inj_conf * src_conf
    else:
        if match_data.get("injury_home_missing", False): score -= 0.4
        if match_data.get("injury_away_missing", False): score -= 0.4
        if match_data.get("injury_source_unreliable", False): score -= 0.2
        if match_data.get("injury_home_missing", False) and match_data.get("injury_away_missing", False):
            score -= 0.15

    return max(0, score)


def score_motivation_clarity(match_data):
    score = 1.0
    if match_data.get("no_coach_statement", False): score -= 0.25
    if match_data.get("motivation_ambiguous", False): score -= 0.25
    if match_data.get("multi_team_linkage", False): score -= 0.2
    mt = match_data.get("match_type", "")
    if match_data.get("no_coach_statement", False) and mt in ["附加赛", "解放者杯末轮", "南美杯末轮"]:
        score -= 0.2
    return max(0, score)


def score_handicap_deviation(lambda_diff, asian_handicap):
    score = 2.0
    if lambda_diff > 1.5 and abs(asian_handicap) < 0.5: score -= 1.2
    elif lambda_diff < -0.15 and asian_handicap < 0: score -= 0.9
    elif abs(lambda_diff) < 0.5 and abs(asian_handicap) >= 1.0: score -= 0.9
    elif 0.5 <= abs(lambda_diff) < 1.0 and abs(asian_handicap) >= 1.5: score -= 0.6
    if abs(lambda_diff) > 1.0 and abs(asian_handicap) < 0.5: score -= 0.4

    # B路线新增：xG差拆扣分
    xg_diff = abs(lambda_diff)
    if xg_diff < 0.1:
        score -= 1.0
    elif xg_diff < 0.3:
        score -= 0.5
    elif xg_diff < 0.5:
        score -= 0.2
    elif xg_diff < 0.8:
        score -= 0.1
    elif xg_diff > 2.0:
        score += 0.3
    elif xg_diff > 1.2:
        score += 0.15

    return max(0, score)


def score_movement_match(handicap_change, physical_direction):
    score = 1.5
    if physical_direction == "away" and handicap_change > 0: score -= 0.4
    elif physical_direction == "home" and handicap_change < 0: score -= 0.4
    if abs(handicap_change) >= 0.5: score -= 0.3
    return max(0, score)


def score_path_consistency(physical_prob, market_prob, sp_missing):
    score = 2.5
    if sp_missing: return max(0, min(score, 1.0))
    if market_prob.get("home_win", 0) == 0 and market_prob.get("away_win", 0) == 0:
        return max(0, min(score, 1.0))
    phy_dir = max(physical_prob, key=physical_prob.get)
    mkt_dir = max(market_prob, key=market_prob.get)
    if phy_dir != mkt_dir:
        score -= 1.0
        if abs(physical_prob[phy_dir] - market_prob[mkt_dir]) > 0.20: score -= 0.4
    else:
        if abs(physical_prob[phy_dir] - market_prob[phy_dir]) > 0.15: score -= 0.4
    return max(0, score)


def score_event_adaptability(match_data):
    score = 1.5
    event = match_data.get("event", "")
    home_league = match_data.get("home_league", "")
    away_league = match_data.get("away_league", "")
    if any(kw in event for kw in ["决赛", "半决赛", "欧协", "欧冠", "欧联"]): score -= 0.5
    if any(kw in event for kw in ["解放者杯", "南美杯"]): score -= 0.5
    if home_league != away_league: score -= 0.3
    return max(0, score)


def apply_veto_rules(scores, final_total):
    # ?????????????????raw_total?????
    if scores['injury_confidence'] <= 0.3:
        final_total -= 0.3
    if scores['motivation_clarity'] <= 0.4:
        final_total -= 0.3
    if scores['event_fit'] <= 0.4:
        final_total -= 0.3
    return max(0, final_total)


def calc_fit_score(match_data, ddi_result, ai_judgment):
    sp_h, sp_d, sp_a = match_data.get("sp_home"), match_data.get("sp_draw"), match_data.get("sp_away")
    sp_missing = not all([sp_h, sp_d, sp_a])
    s1 = score_data_confidence(match_data)
    s2 = score_injury_reliability(match_data)
    s3 = score_motivation_clarity(match_data)
    s4 = score_handicap_deviation(match_data.get("lambda_diff", 0), match_data.get("asian_handicap", 0))
    s5 = score_movement_match(match_data.get("handicap_change", 0), match_data.get("physical_direction", "home"))
    s6 = score_path_consistency(ddi_result["p_physical"], ddi_result.get("p_market", {}), sp_missing)
    s_event_fit = score_event_adaptability(match_data)
    s_ai_penalty = ai_judgment.get("s7_score", 0)
    match_type = match_data.get("match_type", "")
    if match_type in ["附加赛", "解放者杯末轮", "南美杯末轮"]:
        s_ai_penalty = max(s_ai_penalty, 0.5)
    opp_coef = max(ai_judgment.get("opponent_predictability", 1.0), OPPONENT_PREDICTABILITY_MIN)
    raw_total = s1 + s2 + s3 + s4 + s5 + s6 + s_event_fit
    final_total = round((raw_total - s_ai_penalty) * opp_coef * NORMALIZE, 2)
    final_total = apply_veto_rules({'injury_confidence': s2, 'motivation_clarity': s3, 'event_fit': s_event_fit}, final_total)

    if final_total >= 8.0: level = "高贴合"
    elif final_total >= 6.0: level = "中等贴合"
    elif final_total >= 4.0: level = "低贴合"
    else: level = "低贴合熔断"
    return {
        "details": {"1_数据完整度": round(s1,1), "2_伤停确定度": round(s2,1), "3_战意清晰度": round(s3,1),
                    "4_盘口偏离合理性": round(s4,1), "5_临场异动匹配度": round(s5,1),
                    "6_物理市场一致性": round(s6,1), "7_赛事适配度": round(s_event_fit,1),
                    "s7_心理扰动扣分": s_ai_penalty, "对手可预测性系数": opp_coef},
        "raw_total": round(raw_total, 2), "final_total": final_total,
        "level": level, "meltdown": final_total < FIT_SCORE_THRESHOLD_MELTDOWN
    }


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    with open(os.path.join(data_dir, "match_info.json"), encoding="utf-8") as f: match_info = json.load(f)
    with open(os.path.join(data_dir, "ddi_result.json"), encoding="utf-8") as f: ddi_data = json.load(f)
    with open(os.path.join(data_dir, "ai_judgment.json"), encoding="utf-8") as f: ai_data = json.load(f)
    info_map = {m["id"]: m for m in match_info["matches"]}
    ddi_map = {m["id"]: m for m in ddi_data["matches"]}
    ai_map = {m["id"]: m for m in ai_data["matches"]}
    all_ids = set(info_map.keys()) | set(ddi_map.keys()) | set(ai_map.keys())
    valid_ids = set(info_map.keys()) & set(ddi_map.keys()) & set(ai_map.keys())
    dropped = all_ids - valid_ids
    if dropped:
        print(f"  [WARN] {len(dropped)}场比赛被排除（数据不完整）: {sorted(dropped)}")
    results = []
    for mid in valid_ids:
        fit = calc_fit_score(info_map[mid], ddi_map[mid], ai_map[mid])
        results.append({"id": mid, "fit_score": fit})
        status = "MELTDOWN" if fit["meltdown"] else "PASS"
        print(f"  [{mid}] 贴合度{fit['final_total']:.1f} ({fit['level']}) {status}")
    with open(os.path.join(data_dir, "fit_score_result.json"), "w", encoding="utf-8") as f:
        json.dump({"matches": results}, f, ensure_ascii=False, indent=2)
    print(f"\n  [OK] 贴合度评估完成")


if __name__ == "__main__":
    print("=" * 55)
    print("  V3.3.3-Core-Rev1.13 Step 8: 贴合度评估（xG差拆分版）")
    print("=" * 55)
    main()
