import sys, re

path = r"C:\Users\gjj\Desktop\v333\pipeline.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ==============================
# P0: 置信度字段 + P1: 样本量字段
# 在 match_info 构建处插入
# ==============================

old_info_append = """info_matches.append({
                "id": m.get('id', ''),
                "home": m.get('home', ''),
                "away": m.get('away', ''),
                "event": m.get('event', ''),
                "time": m.get('time', ''),
                "sp_home": m.get('sp_home'),
                "sp_draw": m.get('sp_draw'),
                "sp_away": m.get('sp_away'),
                "initial_sp_home": m.get('initial_sp_home'),
                "initial_sp_draw": m.get('initial_sp_draw'),
                "initial_sp_away": m.get('initial_sp_away'),
                "asian_handicap": m.get('asian_handicap', 0),
                "handicap_change": m.get('handicap_change', 0),
                "match_type": m.get('match_type', '常规'),
                "is_home_life_death": m.get('is_home_life_death', False),
                "lambda_diff": 0,
                "physical_direction": "home",
                "predicted_direction": "home",
                "h2h_missing": m.get('h2h_missing', False),
                "xg_last3_missing": m.get('xg_last3_missing', False),
                "xg_season_missing": m.get('xg_season_missing', False),
                "roster_missing": m.get('roster_missing', False),
                "injury_home_missing": m.get('injury_home_missing', False),
                "injury_away_missing": m.get('injury_away_missing', False),
                "injury_source_unreliable": m.get('injury_source_unreliable', False),
                "no_coach_statement": m.get('no_coach_statement', False),
                "motivation_ambiguous": m.get('motivation_ambiguous', False),
                "multi_team_linkage": m.get('multi_team_linkage', False),
                "away_xg_missing": m.get('away_xg_missing', False),
                "home_goals": m.get('home_goals', m.get('home_xg')),
                "home_goals_conceded": m.get('home_goals_conceded', m.get('home_xga')),
                "away_goals": m.get('away_goals', m.get('away_xg')),
                "away_goals_conceded": m.get('away_goals_conceded', m.get('away_xga'))
            })"""

new_info_append = """info_matches.append({
                "id": m.get('id', ''),
                "home": m.get('home', ''),
                "away": m.get('away', ''),
                "event": m.get('event', ''),
                "time": m.get('time', ''),
                "sp_home": m.get('sp_home'),
                "sp_draw": m.get('sp_draw'),
                "sp_away": m.get('sp_away'),
                "initial_sp_home": m.get('initial_sp_home'),
                "initial_sp_draw": m.get('initial_sp_draw'),
                "initial_sp_away": m.get('initial_sp_away'),
                "asian_handicap": m.get('asian_handicap', 0),
                "handicap_change": m.get('handicap_change', 0),
                "match_type": m.get('match_type', '常规'),
                "is_home_life_death": m.get('is_home_life_death', False),
                "lambda_diff": 0,
                "physical_direction": "home",
                "predicted_direction": "home",
                # ===== 数据置信度分层 (P0) =====
                # data_confidence: "api"=API直接返回, "calc"=推算, "infer"=纯推理
                "h2h_confidence": "api" if not m.get('h2h_missing') else "infer",
                "xg_last3_confidence": "calc" if not m.get('xg_last3_missing') else "infer",
                "xg_season_confidence": "api" if not m.get('xg_season_missing') else "infer",
                "roster_confidence": "api" if not m.get('roster_missing') else "infer",
                "injury_home_confidence": "api" if not m.get('injury_home_missing') else "infer",
                "injury_away_confidence": "api" if not m.get('injury_away_missing') else "infer",
                "injury_source_confidence": "calc" if not m.get('injury_source_unreliable') else "infer",
                "motivation_confidence": "calc" if not m.get('motivation_ambiguous') else "infer",
                # ===== 样本量字段 (P1) =====
                "xg_home_sample": m.get('xg_home_sample', 0),
                "xg_away_sample": m.get('xg_away_sample', 0),
                "xg_last3_home_sample": m.get('xg_last3_home_sample', 0),
                "xg_last3_away_sample": m.get('xg_last3_away_sample', 0),
                # xg数据来源赛事类型（用于跨赛事对比检测）
                "xg_home_source_events": m.get('xg_home_source_events', ''),
                "xg_away_source_events": m.get('xg_away_source_events', ''),
                # ===== 保留原有字段 =====
                "h2h_missing": m.get('h2h_missing', False),
                "xg_last3_missing": m.get('xg_last3_missing', False),
                "xg_season_missing": m.get('xg_season_missing', False),
                "roster_missing": m.get('roster_missing', False),
                "injury_home_missing": m.get('injury_home_missing', False),
                "injury_away_missing": m.get('injury_away_missing', False),
                "injury_source_unreliable": m.get('injury_source_unreliable', False),
                "no_coach_statement": m.get('no_coach_statement', False),
                "motivation_ambiguous": m.get('motivation_ambiguous', False),
                "multi_team_linkage": m.get('multi_team_linkage', False),
                "away_xg_missing": m.get('away_xg_missing', False),
                "home_goals": m.get('home_goals', m.get('home_xg')),
                "home_goals_conceded": m.get('home_goals_conceded', m.get('home_xga')),
                "away_goals": m.get('away_goals', m.get('away_xg')),
                "away_goals_conceded": m.get('away_goals_conceded', m.get('away_xga'))
            })"""

if old_info_append in content:
    content = content.replace(old_info_append, new_info_append)
    print("P0+P1: pipeline.py match_info 已更新")
else:
    print("P0+P1: 未找到原 match_info block")
    # 搜索确认
    idx = content.find("info_matches.append({")
    if idx >= 0:
        print(f"  位置 {idx}: 前50字={content[idx:idx+50]}")

# ==============================
# P4: 集成时序完整性检测
# ==============================
old_run_pipeline = """        # 运行全流程分析
        print(f"  运行全流程分析...")"""

new_run_pipeline = """        # 时序完整性检测 (P4)
        from lambda_calc import validate_temporal_integrity
        for m in locked_data.get('matches', []):
            validate_temporal_integrity(m)
        print(f"  [OK] 时序完整性检测完成")

        # 运行全流程分析
        print(f"  运行全流程分析...")"""

if old_run_pipeline in content:
    content = content.replace(old_run_pipeline, new_run_pipeline)
    print("P4: pipeline 时序检测已集成")
else:
    print("P4: 未找到 pipeline 运行标记")
    idx = content.find("运行全流程分析")
    if idx >= 0:
        print(f"  位置 {idx}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("pipeline.py 保存完成")