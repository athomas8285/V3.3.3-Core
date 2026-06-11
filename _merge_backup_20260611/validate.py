# validate.py
# V3.3.3-Core-Rev1.13 Step 5：参数交叉校验（无emoji版）

def validate_lambda_vs_handicap(lambda_h, lambda_a, asian_handicap, match_id, home, away):
    warnings = []
    diff = lambda_h - lambda_a
    if diff > 1.5 and abs(asian_handicap) < 0.5:
        warnings.append(f"严重背离：lambda差+{diff:.2f}（主队碾压），但盘口仅{asian_handicap:+.2f}。")
    elif diff < -0.15 and asian_handicap < 0:
        warnings.append(f"方向背离：lambda差{diff:+.2f}（客队占优），但盘口主让{asian_handicap:+.2f}。")
    elif abs(diff) < 0.5 and abs(asian_handicap) >= 1.0:
        warnings.append(f"盘口过深：lambda差仅{diff:+.2f}，但盘口{asian_handicap:+.2f}。")
    elif 0.5 <= abs(diff) < 1.0 and abs(asian_handicap) >= 1.5:
        warnings.append(f"盘口偏深：lambda差{diff:+.2f}，但盘口{asian_handicap:+.2f}。")
    return warnings


def validate_motivation_cap(motivation_home, motivation_away, match_type):
    warnings = []
    playoff_types = ["附加赛", "解放者杯末轮", "南美杯末轮"]
    cap = 0.05 if match_type in playoff_types else 0.15
    if abs(motivation_home) > cap:
        warnings.append(f"主队战意修正{motivation_home:+.0%}超过硬上限±{cap:.0%}")
    if abs(motivation_away) > cap:
        warnings.append(f"客队战意修正{motivation_away:+.0%}超过硬上限±{cap:.0%}")
    return warnings


def cross_validate(match, lambda_h_final, lambda_a_final, factor_params):
    mid = match["id"]
    home = match["home"]
    away = match["away"]
    asian_handicap = match.get("asian_handicap", 0)
    match_type = match.get("match_type", "")

    all_warnings = []
    w1 = validate_lambda_vs_handicap(lambda_h_final, lambda_a_final, asian_handicap, mid, home, away)
    all_warnings.extend(w1)

    if factor_params and factor_params.get("motivation_home") is not None:
        fp = factor_params
        w2 = validate_motivation_cap(fp["motivation_home"], fp["motivation_away"], match_type)
        all_warnings.extend(w2)

    if all_warnings:
        print(f"  [WARN] Step 5 交叉校验警告:")
        for w in all_warnings:
            print(f"    - {w}")
    else:
        print(f"  [OK] Step 5 交叉校验通过")

    return all_warnings