# auto_pipeline.py
# V3.3.3-Core-Rev1.15 一键全流程：读取 locked_data → 自动生成所有输入 → 运行 pipeline → 输出汇总
# 用法: python auto_pipeline.py
#       或: python auto_pipeline.py --factor-json path/to/factor_params.json

import json, os, sys, subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_match_info(locked_data):
    """从 locked_data 生成 match_info.json（对齐框架 Step 2 → Step 6）"""
    matches = []
    for m in locked_data.get("matches", []):
        matches.append({
            "id": m["id"],
            "home": m["home"],
            "away": m["away"],
            "event": m.get("event", ""),
            "time": m.get("time", ""),
            "sp_home": m.get("sp_home"),
            "sp_draw": m.get("sp_draw"),
            "sp_away": m.get("sp_away"),
            "initial_sp_home": m.get("initial_sp_home"),
            "initial_sp_draw": m.get("initial_sp_draw"),
            "initial_sp_away": m.get("initial_sp_away"),
            "asian_handicap": m.get("asian_handicap", 0),
            "handicap_change": m.get("handicap_change", 0),
            "match_type": m.get("match_type", "常规"),
            "is_home_life_death": m.get("is_home_life_death", False),
            "lambda_diff": 0,
            "physical_direction": "home",
            "predicted_direction": "home",
            "h2h_missing": m.get("h2h_missing", False),
            "xg_last3_missing": m.get("xg_last3_missing", False),
            "xg_season_missing": m.get("xg_season_missing", False),
            "roster_missing": m.get("roster_missing", False),
            "injury_home_missing": m.get("injury_home_missing", False),
            "injury_away_missing": m.get("injury_away_missing", False),
            "injury_source_unreliable": m.get("injury_source_unreliable", False),
            "no_coach_statement": m.get("no_coach_statement", False),
            "motivation_ambiguous": m.get("motivation_ambiguous", False),
            "multi_team_linkage": m.get("multi_team_linkage", False),
            "away_xg_missing": m.get("away_xg_missing", False),
            "home_goals": m.get("home_goals", m.get("home_xg")),
            "home_goals_conceded": m.get("home_goals_conceded", m.get("home_xga")),
            "away_goals": m.get("away_goals", m.get("away_xg")),
            "away_goals_conceded": m.get("away_goals_conceded", m.get("away_xga"))
        })
    return {"matches": matches}


def generate_ai_judgment_placeholder(locked_data):
    """生成 ai_judgment.json 占位（s7_score=0, opponent_predictability=1.0）"""
    matches = []
    for m in locked_data.get("matches", []):
        matches.append({
            "id": m["id"],
            "s7_score": 0,
            "s7_reason": "自动生成，无特殊扰动",
            "opponent_predictability": 1.0,
            "opponent_reason": "",
            "trap_analysis": "",
            "key_risk": ""
        })
    return {"matches": matches}


def generate_default_factors(locked_data):
    """从 locked_data 生成默认 factor_params（所有修正为0，无特殊判断）"""
    matches = []
    for m in locked_data.get("matches", []):
        matches.append({
            "id": m["id"],
            "injury_home": 0.0,
            "injury_away_boost": 0.0,
            "injury_away": 0.0,
            "injury_home_boost": 0.0,
            "motivation_home": 0.0,
            "motivation_away": 0.0,
            "pressure_home": False,
            "pressure_away": False,
            "slack_home": False,
            "slack_away": False,
            "altitude_home": 0.0,
            "altitude_away": 0.0
        })
    return {"matches": matches}


def run_step(script_name, description):
    """运行单个步骤脚本并检查错误"""
    result = subprocess.run(
        [sys.executable, os.path.join(BASE_DIR, script_name)],
        capture_output=False, cwd=BASE_DIR
    )
    if result.returncode != 0:
        print(f"  [ERROR] {script_name} 运行失败 (exit={result.returncode})")
        return False
    return True


def print_summary():
    """读取最终结果并打印汇总"""
    rating_path = os.path.join(DATA_DIR, "rating_result.json")
    if not os.path.exists(rating_path):
        print("  [WARN] 评级结果未生成")
        return

    rating = load_json(rating_path)
    print()
    print("=" * 68)
    print("  最终汇总表")
    print("=" * 68)
    print(f"  {'#':<5}{'ID':<5}{'对阵':<28}{'方向':<8}{'贴合度':<8}{'评级':<10}")
    print(f"  {'-'*64}")
    for i, r in enumerate(rating.get("matches", []), 1):
        vs = f"{r['home']} vs {r['away']}"
        direction = r["direction"]
        warn = "!" if r.get("direction_warning") else ""
        fit = r["fit_score"]
        rating_label = r["rating"]
        print(f"  {i:<5}{r['id']:<5}{vs:<28}{direction+warn:<8}{fit:<8.1f}{rating_label:<10}")
    print("=" * 68)


def main():
    print("=" * 60)
    print("  V3.3.3-Core-Rev1.15 一键全流程")
    print("=" * 60)

    # 检查必要输入
    locked_path = os.path.join(DATA_DIR, "locked_data.json")
    if not os.path.exists(locked_path):
        print(f"  [ERROR] 缺少 {locked_path}")
        print(f"  请先准备 locked_data.json 放入 data/ 目录")
        return

    # 1. 读取 locked_data
    print(f"\n  [1/5] 读取 locked_data.json...")
    locked_data = load_json(locked_path)
    match_count = len(locked_data.get("matches", []))
    print(f"        共 {match_count} 场比赛")

    # 2. 生成 match_info.json
    print(f"  [2/5] 生成 match_info.json...")
    match_info = generate_match_info(locked_data)
    save_json(match_info, os.path.join(DATA_DIR, "match_info.json"))
    print(f"        -> data/match_info.json")

    # 3. 检查/生成 factor_params.json
    factor_path = os.path.join(DATA_DIR, "factor_params.json")
    if "--factor-json" in sys.argv:
        idx = sys.argv.index("--factor-json")
        custom_path = sys.argv[idx + 1]
        if os.path.exists(custom_path):
            import shutil
            shutil.copy(custom_path, factor_path)
            print(f"  [3/5] 使用自定义因子参数: {custom_path}")
        else:
            print(f"  [3/5] 自定义因子文件不存在，生成默认值")
            save_json(generate_default_factors(locked_data), factor_path)
    elif os.path.exists(factor_path):
        print(f"  [3/5] 使用已有 factor_params.json")
    else:
        print(f"  [3/5] factor_params.json 不存在，生成默认值（全0）")
        save_json(generate_default_factors(locked_data), factor_path)
        print(f"        -> data/factor_params.json (默认值)")
        print(f"        [提示] 如需精确因子参数，请编辑 factor_params.json 后重新运行")

    # 4. 检查/生成 ai_judgment.json
    ai_path = os.path.join(DATA_DIR, "ai_judgment.json")
    if os.path.exists(ai_path):
        # 检查是否为占位内容（smart_factors 已生成则保留）
        try:
            existing = load_json(ai_path)
            sample = existing.get("matches", [{}])[0]
            is_placeholder = (sample.get("trap_analysis", "") == "" and
                              sample.get("opponent_reason", "") == "" and
                              sample.get("s7_reason", "") == "自动生成，无特殊扰动")
            if is_placeholder:
                print(f"  [4/5] 已有 ai_judgment.json 但为占位内容，由 smart_factors 重新生成")
                save_json(generate_ai_judgment_placeholder(locked_data), ai_path)
            else:
                print(f"  [4/5] 检测到 smart_factors 已生成 ai_judgment.json，跳过覆写")
        except Exception:
            print(f"  [4/5] ai_judgment.json 读取异常，重新生成占位")
            save_json(generate_ai_judgment_placeholder(locked_data), ai_path)
    else:
        print(f"  [4/5] ai_judgment.json 不存在，生成占位")
        save_json(generate_ai_judgment_placeholder(locked_data), ai_path)

    # 5. 运行全流程
    print(f"  [5/5] 运行全流程分析...")
    print(f"  {'='*58}")

    if not run_step("run_all.py", "全流程"):
        print(f"\n  [ERROR] 分析失败")
        return

    print(f"\n  [OK] 全流程分析完成")
    print_summary()

    # 6. 从竞彩网获取实时赔率
    print(f"\n  [6/7] 获取竞彩网实时赔率...")
    if not run_step("fetch_jczq.py", "竞彩网数据"):
        print(f"         [WARN] 竞彩网数据获取失败，跳过 (不影响核心流程)")
    else:
        print(f"        -> data/raw_jczq.json")

        # 7. 将竞彩网赔率写入 match_info.json / locked_data.json
        print(f"  [7/7] 同步竞彩网赔率到数据文件...")
        if not run_step("enrich_odds.py", "赔率同步"):
            print(f"         [WARN] 赔率同步失败，跳过 (不影响核心流程)")
        else:
            print(f"        -> match_info.json / locked_data.json 已包含 jc_sp_ 等字段")


if __name__ == "__main__":
    main()
