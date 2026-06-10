# -*- coding: utf-8 -*-
import json, os, sys

BASE = "C:\\Users\\gjj\\Desktop\\v333"
DATA = os.path.join(BASE, "data")

# ===== locked_data =====
locked = {"matches": [
  {
    "id": "003",
    "event": "国际足球友谊赛",
    "time": "2026-05-31 18:25",
    "home": "日本",
    "away": "冰岛",
    "home_league": "国际赛",
    "away_league": "国际赛",
    "sp_home": 1.13, "sp_draw": 6.05, "sp_away": 13.00,
    "initial_sp_home": None, "initial_sp_draw": None, "initial_sp_away": None,
    "jc_handicap": -2, "asian_handicap": -2.0, "handicap_change": 0.25,
    "home_xg": 2.4, "home_xga": 0.9, "away_xg": 0.8, "away_xga": 1.8,
    "home_goals": 2.4, "home_goals_conceded": 0.9,
    "away_goals": 0.8, "away_goals_conceded": 1.8,
    "h2h_missing": True, "xg_last3_missing": True, "xg_season_missing": True,
    "roster_missing": False,
    "injury_home_missing": False, "injury_away_missing": False,
    "injury_source_unreliable": False, "no_coach_statement": False,
    "motivation_ambiguous": True, "multi_team_linkage": False,
    "match_type": "友谊赛", "is_home_life_death": False,
    "away_xg_missing": True
  },
  {
    "id": "004",
    "event": "瑞典超第12轮",
    "time": "2026-05-31 20:00",
    "home": "韦斯特罗",
    "away": "哥德堡",
    "home_league": "瑞典超",
    "away_league": "瑞典超",
    "sp_home": 2.45, "sp_draw": 3.05, "sp_away": 2.54,
    "initial_sp_home": None, "initial_sp_draw": None, "initial_sp_away": None,
    "jc_handicap": -1, "asian_handicap": 0, "handicap_change": 0,
    "home_xg": 1.15, "home_xga": 1.45, "away_xg": 0.98, "away_xga": 1.62,
    "home_goals": 1.18, "home_goals_conceded": 1.45,
    "away_goals": 0.91, "away_goals_conceded": 1.64,
    "h2h_missing": False, "xg_last3_missing": False, "xg_season_missing": False,
    "roster_missing": False,
    "injury_home_missing": False, "injury_away_missing": False,
    "injury_source_unreliable": False, "no_coach_statement": False,
    "motivation_ambiguous": False, "multi_team_linkage": False,
    "match_type": "常规", "is_home_life_death": False,
    "away_xg_missing": False
  },
  {
    "id": "005",
    "event": "瑞典超第12轮",
    "time": "2026-05-31 20:00",
    "home": "赫根",
    "away": "哈马比",
    "home_league": "瑞典超",
    "away_league": "瑞典超",
    "sp_home": 2.79, "sp_draw": 3.45, "sp_away": 2.08,
    "initial_sp_home": None, "initial_sp_draw": None, "initial_sp_away": None,
    "jc_handicap": 1, "asian_handicap": 0.5, "handicap_change": 0.25,
    "home_xg": 1.85, "home_xga": 1.55, "away_xg": 1.92, "away_xga": 1.10,
    "home_goals": 1.73, "home_goals_conceded": 1.64,
    "away_goals": 1.82, "away_goals_conceded": 1.09,
    "h2h_missing": False, "xg_last3_missing": False, "xg_season_missing": False,
    "roster_missing": False,
    "injury_home_missing": False, "injury_away_missing": False,
    "injury_source_unreliable": False, "no_coach_statement": False,
    "motivation_ambiguous": False, "multi_team_linkage": False,
    "match_type": "常规", "is_home_life_death": False,
    "away_xg_missing": False
  },
  {
    "id": "006",
    "event": "瑞典超第12轮",
    "time": "2026-05-31 20:00",
    "home": "代格福什",
    "away": "布鲁马波",
    "home_league": "瑞典超",
    "away_league": "瑞典超",
    "sp_home": 2.10, "sp_draw": 3.15, "sp_away": 2.98,
    "initial_sp_home": None, "initial_sp_draw": None, "initial_sp_away": None,
    "jc_handicap": -1, "asian_handicap": -0.25, "handicap_change": 0.25,
    "home_xg": 1.05, "home_xga": 1.80, "away_xg": 1.35, "away_xga": 1.45,
    "home_goals": 0.91, "home_goals_conceded": 1.82,
    "away_goals": 1.27, "away_goals_conceded": 1.45,
    "h2h_missing": False, "xg_last3_missing": False, "xg_season_missing": False,
    "roster_missing": False,
    "injury_home_missing": False, "injury_away_missing": False,
    "injury_source_unreliable": False, "no_coach_statement": False,
    "motivation_ambiguous": False, "multi_team_linkage": False,
    "match_type": "常规", "is_home_life_death": False,
    "away_xg_missing": False
  },
  {
    "id": "007",
    "event": "国际足球友谊赛",
    "time": "2026-05-31 21:00",
    "home": "瑞士",
    "away": "约旦",
    "home_league": "国际赛",
    "away_league": "国际赛",
    "sp_home": None, "sp_draw": None, "sp_away": None,
    "initial_sp_home": None, "initial_sp_draw": None, "initial_sp_away": None,
    "jc_handicap": -2, "asian_handicap": -2.0, "handicap_change": 0.25,
    "home_xg": 2.1, "home_xga": 0.8, "away_xg": 1.2, "away_xga": 1.6,
    "home_goals": 2.1, "home_goals_conceded": 0.8,
    "away_goals": 1.2, "away_goals_conceded": 1.6,
    "h2h_missing": True, "xg_last3_missing": True, "xg_season_missing": True,
    "roster_missing": False,
    "injury_home_missing": False, "injury_away_missing": False,
    "injury_source_unreliable": False, "no_coach_statement": False,
    "motivation_ambiguous": True, "multi_team_linkage": False,
    "match_type": "友谊赛", "is_home_life_death": False,
    "away_xg_missing": True
  },
  {
    "id": "008",
    "event": "芬超第12轮",
    "time": "2026-05-31 21:00",
    "home": "AC奥卢",
    "away": "雅罗",
    "home_league": "芬超",
    "away_league": "芬超",
    "sp_home": 1.50, "sp_draw": 3.90, "sp_away": 4.85,
    "initial_sp_home": None, "initial_sp_draw": None, "initial_sp_away": None,
    "jc_handicap": -1, "asian_handicap": -1.0, "handicap_change": 0.25,
    "home_xg": 1.85, "home_xga": 0.95, "away_xg": 1.12, "away_xga": 1.65,
    "home_goals": 1.9, "home_goals_conceded": 0.9,
    "away_goals": 1.1, "away_goals_conceded": 1.7,
    "h2h_missing": True, "xg_last3_missing": False, "xg_season_missing": False,
    "roster_missing": False,
    "injury_home_missing": True, "injury_away_missing": True,
    "injury_source_unreliable": True, "no_coach_statement": True,
    "motivation_ambiguous": True, "multi_team_linkage": False,
    "match_type": "常规", "is_home_life_death": False,
    "away_xg_missing": False
  },
  {
    "id": "009",
    "event": "国际足球友谊赛",
    "time": "2026-05-31 22:00",
    "home": "捷克",
    "away": "科索沃",
    "home_league": "国际赛",
    "away_league": "国际赛",
    "sp_home": 1.52, "sp_draw": 3.64, "sp_away": 5.10,
    "initial_sp_home": None, "initial_sp_draw": None, "initial_sp_away": None,
    "jc_handicap": -1, "asian_handicap": -1.0, "handicap_change": 0.25,
    "home_xg": 1.33, "home_xga": 0.67, "away_xg": 0.9, "away_xga": 2.2,
    "home_goals": 1.33, "home_goals_conceded": 0.67,
    "away_goals": 0.9, "away_goals_conceded": 2.2,
    "h2h_missing": True, "xg_last3_missing": True, "xg_season_missing": True,
    "roster_missing": False,
    "injury_home_missing": False, "injury_away_missing": False,
    "injury_source_unreliable": False, "no_coach_statement": True,
    "motivation_ambiguous": True, "multi_team_linkage": False,
    "match_type": "友谊赛", "is_home_life_death": False,
    "away_xg_missing": True
  }
]}

with open(os.path.join(DATA, "locked_data.json"), "w", encoding="utf-8") as f:
    json.dump(locked, f, ensure_ascii=False, indent=2)
print("locked_data.json OK")

# ===== match_info =====
info = {"matches": []}
for m in locked["matches"]:
    diff = m["home_xg"] * m["away_xga"] - m["away_xg"] * m["home_xga"]
    info["matches"].append({
        "id": m["id"],
        "home": m["home"],
        "away": m["away"],
        "event": m["event"],
        "time": m["time"],
        "home_league": m["home_league"],
        "away_league": m["away_league"],
        "sp_home": m["sp_home"],
        "sp_draw": m["sp_draw"],
        "sp_away": m["sp_away"],
        "initial_sp_home": m["initial_sp_home"],
        "initial_sp_draw": m["initial_sp_draw"],
        "initial_sp_away": m["initial_sp_away"],
        "jc_handicap": m["jc_handicap"],
        "asian_handicap": m["asian_handicap"],
        "handicap_change": m["handicap_change"],
        "lambda_diff": round(diff / 1.35, 4),
        "h2h_missing": m["h2h_missing"],
        "xg_last3_missing": m["xg_last3_missing"],
        "xg_season_missing": m["xg_season_missing"],
        "roster_missing": m["roster_missing"],
        "injury_home_missing": m["injury_home_missing"],
        "injury_away_missing": m["injury_away_missing"],
        "injury_source_unreliable": m["injury_source_unreliable"],
        "no_coach_statement": m["no_coach_statement"],
        "motivation_ambiguous": m["motivation_ambiguous"],
        "multi_team_linkage": m["multi_team_linkage"],
        "match_type": m["match_type"],
        "is_home_life_death": m["is_home_life_death"],
        "away_xg_missing": m["away_xg_missing"],
        "physical_direction": "home" if diff > 0 else "away",
        "predicted_direction": "home" if diff > 0 else "away",
        "home_xg": m["home_xg"],
        "home_xga": m["home_xga"],
        "away_xg": m["away_xg"],
        "away_xga": m["away_xga"],
        "home_goals": m["home_goals"],
        "home_goals_conceded": m["home_goals_conceded"],
        "away_goals": m["away_goals"],
        "away_goals_conceded": m["away_goals_conceded"],
    })

with open(os.path.join(DATA, "match_info.json"), "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=2)
print("match_info.json OK")

# ===== factor_params =====
factors_map = {
    "003":  {"injury_home": 0, "injury_away_boost": 0, "injury_away": 0, "injury_home_boost": 0,
             "motivation_home": 0.03, "motivation_away": 0.02,
             "pressure_home": False, "pressure_away": False,
             "slack_home": False, "slack_away": False,
             "altitude_home": 0, "altitude_away": 0},
    "004":  {"injury_home": 0, "injury_away_boost": 0.08, "injury_away": -0.12, "injury_home_boost": 0,
             "motivation_home": 0.05, "motivation_away": 0.08,
             "pressure_home": False, "pressure_away": False,
             "slack_home": False, "slack_away": False,
             "altitude_home": 0, "altitude_away": 0},
    "005":  {"injury_home": -0.03, "injury_away_boost": 0, "injury_away": 0, "injury_home_boost": 0,
             "motivation_home": 0.08, "motivation_away": 0.08,
             "pressure_home": False, "pressure_away": False,
             "slack_home": False, "slack_away": False,
             "altitude_home": 0, "altitude_away": 0},
    "006":  {"injury_home": 0, "injury_away_boost": 0, "injury_away": 0, "injury_home_boost": 0,
             "motivation_home": 0.08, "motivation_away": 0.03,
             "pressure_home": False, "pressure_away": False,
             "slack_home": False, "slack_away": False,
             "altitude_home": 0, "altitude_away": 0},
    "007":  {"injury_home": 0, "injury_away_boost": 0, "injury_away": 0, "injury_home_boost": 0,
             "motivation_home": 0.02, "motivation_away": 0.05,
             "pressure_home": False, "pressure_away": False,
             "slack_home": True, "slack_away": False,
             "altitude_home": 0, "altitude_away": 0},
    "008":  {"injury_home": 0, "injury_away_boost": 0, "injury_away": 0, "injury_home_boost": 0,
             "motivation_home": 0.08, "motivation_away": 0.08,
             "pressure_home": False, "pressure_away": False,
             "slack_home": False, "slack_away": False,
             "altitude_home": 0, "altitude_away": 0},
    "009":  {"injury_home": 0, "injury_away_boost": 0.08, "injury_away": -0.10, "injury_home_boost": 0,
             "motivation_home": 0.03, "motivation_away": 0.03,
             "pressure_home": False, "pressure_away": False,
             "slack_home": False, "slack_away": False,
             "altitude_home": 0, "altitude_away": 0},
}

factors_list = []
for mid in ["003","004","005","006","007","008","009"]:
    item = {"id": mid, **factors_map[mid]}
    factors_list.append(item)

with open(os.path.join(DATA, "factor_params.json"), "w", encoding="utf-8") as f:
    json.dump({"matches": factors_list}, f, ensure_ascii=False, indent=2)
print("factor_params.json OK")

# ===== ai_judgment =====
ai_map = {
    "003": {
        "s7_score": 0.5,
        "s7_reason": "友谊赛性质，双方均以考察阵容为主；战意不明确且无主帅明确表态",
        "opponent_predictability": 0.95,
        "opponent_reason": "主队视角：冰岛FIFA排名78，实力差距大但数据完整；客队视角：日本实力碾压",
        "trap_analysis": "主让2球深盘伴随盘口从1.75升至2.0，存在诱上可能；日本友谊赛未必全力进攻",
        "key_risk": "友谊赛性质下日本可能大规模轮换；xG数据缺失，物理面判断依赖实际进球替代"
    },
    "004": {
        "s7_score": 0,
        "s7_reason": "无特殊扰动，常规联赛",
        "opponent_predictability": 0.96,
        "opponent_reason": "主队视角：哥德堡头号射手贝里缺阵，进攻端受损严重；客队视角：韦斯特罗中游球队表现稳定",
        "trap_analysis": "平手盘无明显诱盘特征，盘口与实力匹配",
        "key_risk": "哥德堡头号射手贝里缺阵，进攻端依赖度极高；初盘SP缺失，赔率动态修正不触发"
    },
    "005": {
        "s7_score": 0,
        "s7_reason": "常规联赛，环境稳定",
        "opponent_predictability": 0.98,
        "opponent_reason": "双方数据完整，排名接近，表现可预测",
        "trap_analysis": "客让0.5球盘口从0.25升至0.5，资金流向客队；但哈马比近期防守稳固，升盘可能真实看好",
        "key_risk": "赫根后卫耶博阿缺阵；xG高度接近(1.85 vs 1.92)，可能触发平局再分配"
    },
    "006": {
        "s7_score": 0,
        "s7_reason": "常规联赛，环境稳定",
        "opponent_predictability": 0.97,
        "opponent_reason": "双方数据完整，表现符合预期",
        "trap_analysis": "主让0.25盘口从平手升至0.25，结合代格福什近5场不胜的基本面，诱主可能较大",
        "key_risk": "代格福什近5场不胜状态极差，进攻哑火(近3场场均xG仅0.67)；保级战意与实际状态存在背离"
    },
    "007": {
        "s7_score": 0.5,
        "s7_reason": "友谊赛性质，瑞士主帅暗示大规模轮换；扎卡、阿坎吉可能轮休",
        "opponent_predictability": 0.93,
        "opponent_reason": "主队视角：约旦数据不完整，亚洲杯后状态不明；客队视角：瑞士轮换幅度未知",
        "trap_analysis": "主让2球深盘伴随盘口从1.75升至2.0，存在诱上可能；瑞士友谊赛常有赢球输盘惯例",
        "key_risk": "SP胜平负未开售，DDI校准跳过；瑞士主帅暗示大规模轮换；xG数据缺失；约旦具备杯赛爆冷属性"
    },
    "008": {
        "s7_score": 0,
        "s7_reason": "常规联赛，环境稳定",
        "opponent_predictability": 0.92,
        "opponent_reason": "双方伤停信息均缺失，对手可预测性降低；芬超数据源可靠性一般",
        "trap_analysis": "主让1球盘口从0.75升至1.0，结合AC奥卢近期状态火热(近5场4胜1平)，升盘合理",
        "key_risk": "双方伤停信息均缺失；芬超数据源不可靠；主帅表态缺失；战意判断存在不确定性"
    },
    "009": {
        "s7_score": 0.5,
        "s7_reason": "友谊赛性质，双方均以考察阵容为主；主帅表态缺失",
        "opponent_predictability": 0.94,
        "opponent_reason": "主队视角：科索沃FIFA排名115，穆里奇缺阵影响大；客队视角：希克出战存疑",
        "trap_analysis": "主让1球盘口从0.75升至1.0，捷克实力占优，升盘合理；友谊赛需警惕赢球输盘",
        "key_risk": "xG数据全部缺失，物理面判断依赖实际进球替代；穆里奇(科索沃前锋)缺阵；希克(捷克前锋)出战存疑"
    }
}

ai_list = []
for mid in ["003","004","005","006","007","008","009"]:
    item = {"id": mid, **ai_map[mid]}
    ai_list.append(item)

with open(os.path.join(DATA, "ai_judgment.json"), "w", encoding="utf-8") as f:
    json.dump({"matches": ai_list}, f, ensure_ascii=False, indent=2)
print("ai_judgment.json OK")

print("\nAll files generated successfully!")
