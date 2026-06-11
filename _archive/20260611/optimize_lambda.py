import sys

path = r"C:\Users\gjj\Desktop\v333\lambda_calc.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ==============================
# P1: 增加样本量感知的λ计算
# ==============================

old_calc = """def calc_initial_lambda(home_xg, home_xga, away_xg, away_xga, home_league, away_league):
    params = {
        "主队xG": home_xg, "主队xGA": home_xga,
        "客队xG": away_xg, "客队xGA": away_xga,
        "主队联赛": home_league, "客队联赛": away_league,
    }
    missing = [k for k, v in params.items() if v is None]
    if missing:
        raise ValueError(f"λ 计算数据缺失: {', '.join(missing)}")

    home_league_avg = get_league_avg_xga(home_league)
    away_league_avg = get_league_avg_xga(away_league)

    if home_league != away_league:
        home_rate = LEAGUE_EXCHANGE_RATE.get(home_league, 1.0)
        away_rate = LEAGUE_EXCHANGE_RATE.get(away_league, 1.0)
        home_league_avg = home_league_avg * home_rate
        away_league_avg = away_league_avg * away_rate

    lambda_h = home_xg * away_xga / home_league_avg
    lambda_a = away_xg * home_xga / away_league_avg

    return lambda_h, lambda_a"""

new_calc = """def _confidence_scale(sample_size, source_events, match_event):
    """根据样本量和赛事来源计算置信度缩放系数 (0~1)"""
    if sample_size >= 15:
        base = 1.0
    elif sample_size >= 10:
        base = 0.95
    elif sample_size >= 5:
        base = 0.85
    elif sample_size >= 3:
        base = 0.75
    elif sample_size >= 1:
        base = 0.60
    else:
        return 0.40  # 无样本

    # 跨赛事惩罚
    if source_events and match_event:
        src_types = set(e.strip() for e in source_events.split(",") if e.strip())
        # 如果来源赛事与当前赛事不同类（友谊赛vs正式赛）
        is_friendly = any("友谊" in e for e in src_types) and "友谊" not in match_event
        is_cross_type = (any("友谊" in e for e in src_types) != ("友谊" in match_event))
        if is_cross_type:
            base *= 0.75
            print(f"    [WARN] xG来自友谊赛但当前比赛为正式赛（或反之），置信度降至{base:.2f}")

    return base


def calc_initial_lambda(home_xg, home_xga, away_xg, away_xga, home_league, away_league,
                         home_sample=0, away_sample=0, home_source_events="", away_source_events="",
                         match_event=""):
    params = {
        "主队xG": home_xg, "主队xGA": home_xga,
        "客队xG": away_xg, "客队xGA": away_xga,
        "主队联赛": home_league, "客队联赛": away_league,
    }
    missing = [k for k, v in params.items() if v is None]
    if missing:
        raise ValueError(f"λ 计算数据缺失: {', '.join(missing)}")

    home_league_avg = get_league_avg_xga(home_league)
    away_league_avg = get_league_avg_xga(away_league)

    if home_league != away_league:
        home_rate = LEAGUE_EXCHANGE_RATE.get(home_league, 1.0)
        away_rate = LEAGUE_EXCHANGE_RATE.get(away_league, 1.0)
        home_league_avg = home_league_avg * home_rate
        away_league_avg = away_league_avg * away_rate

    lambda_h = home_xg * away_xga / home_league_avg
    lambda_a = away_xg * home_xga / away_league_avg

    # P1: 计算λ置信度
    h_conf = _confidence_scale(home_sample, home_source_events, match_event)
    a_conf = _confidence_scale(away_sample, away_source_events, match_event)
    lambda_confidence = round((h_conf + a_conf) / 2, 3)

    return lambda_h, lambda_a, lambda_confidence"""

if old_calc in content:
    content = content.replace(old_calc, new_calc)
    print("P1: lambda_calc 样本量感知 + 跨赛事检测已添加")
else:
    print("P1: 未找到 calc_initial_lambda")
    idx = content.find("def calc_initial_lambda")
    if idx >= 0:
        print(f"  位置 {idx}")

# ==============================
# P2: 跨赛事检测函数
# ==============================

p2_func = """

# ===== P2: 跨赛事xG混用检测 =====
def detect_cross_tournament_xg(match_event, home_source_events, away_source_events):
    """检测xG是否来自与当前比赛不同类型的赛事"""
    warnings = []
    if not match_event:
        return warnings
    for side, sources in [("home", home_source_events), ("away", away_source_events)]:
        if not sources:
            continue
        src_list = [s.strip() for s in sources.split(",") if s.strip()]
        for src in src_list:
            src_is_friendly = "友谊" in src
            match_is_friendly = "友谊" in match_event
            if src_is_friendly != match_is_friendly:
                warnings.append(f"{side}: xG来源[{src}]与当前赛事[{match_event}]类型不同")
    return warnings
"""

content += p2_func

# 更新 alt 函数签名
old_alt = """def calc_initial_lambda_alt(home_goals, home_goals_conceded,
                             away_goals, away_goals_conceded,
                             home_league, away_league):
    return calc_initial_lambda(
        home_xg=home_goals, home_xga=home_goals_conceded,
        away_xg=away_goals, away_xga=away_goals_conceded,
        home_league=home_league, away_league=away_league
    )"""

new_alt = """def calc_initial_lambda_alt(home_goals, home_goals_conceded,
                             away_goals, away_goals_conceded,
                             home_league, away_league,
                             home_sample=0, away_sample=0,
                             home_source_events="", away_source_events="",
                             match_event=""):
    return calc_initial_lambda(
        home_xg=home_goals, home_xga=home_goals_conceded,
        away_xg=away_goals, away_xga=away_goals_conceded,
        home_league=home_league, away_league=away_league,
        home_sample=home_sample, away_sample=away_sample,
        home_source_events=home_source_events, away_source_events=away_source_events,
        match_event=match_event
    )"""

if old_alt in content:
    content = content.replace(old_alt, new_alt)
    print("P2: alt函数签名已更新")
else:
    print("P2: 未找到 alt 函数")

# 在 main 中打印 λ 置信度
old_main_print = 'print(f"  [{mid}] λ: {lh:.4f}/{la:.4f} (diff={lh-la:+.4f})")'
new_main_print = 'print(f"  [{mid}] λ: {lh:.4f}/{la:.4f} (diff={lh-la:+.4f}) conf={conf}")'

if old_main_print in content:
    content = content.replace(old_main_print, new_main_print)
    print("P1: main输出λ置信度")
else:
    idx = content.find("λ: {lh:.4f}")
    if idx >= 0:
        print(f"  main行: {content[idx:idx+80]}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("lambda_calc.py 保存完成")