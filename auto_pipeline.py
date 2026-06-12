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
    print("=" * 68)
    print("  V3.3.3-Core-Rev1.15 全面采集 + 分析流程")
    print("=" * 68)
