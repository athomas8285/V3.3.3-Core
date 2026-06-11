# parser.py
import re, json

LEAGUE_MAP = {
    '英格兰足球超级联赛': '英超', '西班牙足球甲级联赛': '西甲',
    '意大利足球甲级联赛': '意甲', '德国足球甲级联赛': '德甲',
    '法国足球甲级联赛': '法甲', '荷兰足球甲级联赛': '荷甲',
    '葡萄牙足球超级联赛': '葡超', '葡萄牙超级联赛': '葡超',
    '葡萄牙甲级联赛': '葡甲', '比利时足球甲级联赛': '比甲',
    '韩国K2联赛': '韩K2', '阿根廷甲级联赛': '阿甲',
    '巴西甲级联赛': '巴甲', '巴拉圭甲级联赛': '巴拉圭甲',
    '秘鲁甲级联赛': '秘鲁甲', '智利甲级联赛': '智利甲',
    '哥伦比亚甲级联赛': '哥伦甲', '乌拉圭甲级联赛': '乌甲',
    '厄瓜多尔甲级联赛': '厄瓜多尔甲', '玻利维亚甲级联赛': '玻利维亚甲',
    '委内瑞拉甲级联赛': '委内瑞拉超', '墨西哥足球超级联赛': '墨超',
    '国际足联FIFA': '国际足联FIFA',
}


def extract_matches(text):
    matches = re.split(r'【场次\s*(\d+)\s*】', text)
    result = []
    for i in range(1, len(matches), 2):
        if i + 1 < len(matches):
            result.append((matches[i], matches[i + 1].strip()))
    if not result:
        blocks = re.split(r'【一、比赛基本信息】', text)
        blocks = [b.strip() for b in blocks if b.strip()]
        for i, block in enumerate(blocks, 1):
            mid = re.search(r'场次\s*(\d+)', block)
            mid = mid.group(1) if mid else f'{i:03d}'
            result.append((mid, '【一、比赛基本信息】' + block))
    return result


def parse_single_match(match_id, text):
    data = {}
    def find(pattern, default=''):
        m = re.search(pattern, text)
        return m.group(1).strip() if m else default
    data['id'] = match_id
    data['event'] = find(r'赛事名称[：:]\s*(.+)')
    data['home'] = find(r'主队[（(]全称[）)][：:]\s*(.+)')
    data['away'] = find(r'客队[（(]全称[）)][：:]\s*(.+)')
    data['time'] = find(r'比赛时间[（(]北京时间[）)][：:]\s*(.+)')
    sp_line = find(r'即时胜平负SP[：:]\s*(.+)')
    sp_match = re.search(r'主胜\s*([\d.]+)\s*/\s*平局\s*([\d.]+)\s*/\s*客胜\s*([\d.]+)', sp_line)
    if sp_match:
        data['sp_home'] = float(sp_match.group(1))
        data['sp_draw'] = float(sp_match.group(2))
        data['sp_away'] = float(sp_match.group(3))
    else:
        data['sp_home'] = None; data['sp_draw'] = None; data['sp_away'] = None
    jc_line = find(r'竞彩让球数[（(][^）)]*[）)][：:]\s*(.+)')
    jc_num = re.search(r'([+-]?\d+)', jc_line)
    data['jc_handicap'] = int(jc_num.group(1)) if jc_num else 0
    asian_line = find(r'即时亚洲让球盘[（(]含水位[）)][：:]\s*(.+)')
    asian_match = re.search(r'主让\s*([\d.]+)\s*球.*/\s*主水\s*([\d.]+)\s*/\s*客水\s*([\d.]+)', asian_line)
    if not asian_match:
        asian_match = re.search(r'客让\s*([\d.]+)\s*球.*/\s*主水\s*([\d.]+)\s*/\s*客水\s*([\d.]+)', asian_line)
        if asian_match:
            data['asian_handicap'] = -float(asian_match.group(1))
        else:
            asian_match = re.search(r'平手\s*/\s*主水\s*([\d.]+)\s*/\s*客水\s*([\d.]+)', asian_line)
            data['asian_handicap'] = 0 if asian_match else 0
    else:
        data['asian_handicap'] = float(asian_match.group(1))
    initial_line = find(r'初盘亚洲让球盘[：:]\s*(.+)')
    init_match = re.search(r'主让\s*([\d.]+)', initial_line)
    if not init_match:
        init_match = re.search(r'客让\s*([\d.]+)', initial_line)
        init_val = -float(init_match.group(1)) if init_match else 0
    else:
        init_val = float(init_match.group(1))
    if init_val is not None and 'asian_handicap' in data:
        data['handicap_change'] = round(data['asian_handicap'] - init_val, 2)
    else:
        data['handicap_change'] = 0
    xg_h = re.search(r'主队赛季场均xG[：:]\s*([\d.]+)', text)
    xg_a = re.search(r'客队赛季场均xG[：:]\s*([\d.]+)', text)
    xga_h = re.search(r'主队赛季场均xGA[：:]\s*([\d.]+)', text)
    xga_a = re.search(r'客队赛季场均xGA[：:]\s*([\d.]+)', text)
    data['home_xg'] = float(xg_h.group(1)) if xg_h else None
    data['away_xg'] = float(xg_a.group(1)) if xg_a else None
    data['home_xga'] = float(xga_h.group(1)) if xga_h else None
    data['away_xga'] = float(xga_a.group(1)) if xga_a else None
    goals_h = re.search(r'主队赛季场均实际进球[：:]\s*([\d.]+)', text)
    goals_a = re.search(r'客队赛季场均实际进球[：:]\s*([\d.]+)', text)
    conceded_h = re.search(r'主队赛季场均实际失球[：:]\s*([\d.]+)', text)
    conceded_a = re.search(r'客队赛季场均实际失球[：:]\s*([\d.]+)', text)
    data['home_goals'] = float(goals_h.group(1)) if goals_h else data.get('home_xg')
    data['away_goals'] = float(goals_a.group(1)) if goals_a else data.get('away_xg')
    data['home_goals_conceded'] = float(conceded_h.group(1)) if conceded_h else data.get('home_xga')
    data['away_goals_conceded'] = float(conceded_a.group(1)) if conceded_a else data.get('away_xga')
    league_line = find(r'两队所在联赛名称[（(]主/客[）)][：:]\s*(.+)')
    leagues = re.split(r'\s*/\s*', league_line)
    raw_home = leagues[0].strip() if len(leagues) > 0 else '默认'
    raw_away = leagues[1].strip() if len(leagues) > 1 else '默认'
    data['home_league'] = LEAGUE_MAP.get(raw_home, raw_home)
    data['away_league'] = LEAGUE_MAP.get(raw_away, raw_away)
    data['home_motivation_type'] = find(r'主队战意类型[：:]\s*(.+)').split('（')[0].strip()
    data['away_motivation_type'] = find(r'客队战意类型[：:]\s*(.+)').split('（')[0].strip()
    data['is_playoff'] = '是' in find(r'是否附加赛[／/]解放者杯或南美杯小组赛末轮[？?][：:]\s*(.+)', '否')
    data['coach_statement'] = find(r'赛前主帅表态[：:]\s*(.+)')
    data['coach_statement'] = data['coach_statement'] if data['coach_statement'] and '缺失' not in data['coach_statement'] else ''
    altitude_line = find(r'比赛场地海拔[：:]\s*(.+)')
    altitude = re.search(r'([\d.]+)\s*米?', altitude_line)
    data['altitude'] = float(altitude.group(1)) if altitude else 0
    data['is_last_round'] = '是' in find(r'是否联赛末轮[？?][：:]\s*(.+)', '否')
    return data


def build_locked_data(matches):
    result = []
    for m in matches:
        result.append({
            "id": m['id'], "home": m['home'], "away": m['away'],
            "event": m['event'], "time": m['time'],
            "home_xg": m['home_xg'], "home_xga": m['home_xga'],
            "away_xg": m['away_xg'], "away_xga": m['away_xga'],
            "home_league": m['home_league'], "away_league": m['away_league'],
            "jc_handicap": m['jc_handicap'],
            "sp_home": m['sp_home'], "sp_draw": m['sp_draw'], "sp_away": m['sp_away'],
            "asian_handicap": m['asian_handicap'], "handicap_change": m['handicap_change'],
            "h2h_missing": False, "xg_last3_missing": False,
            "xg_season_missing": m['home_xg'] is None, "roster_missing": False,
            "injury_home_missing": False, "injury_away_missing": False,
            "injury_source_unreliable": False,
            "no_coach_statement": not bool(m['coach_statement']),
            "motivation_ambiguous": False, "multi_team_linkage": False,
            "match_type": "附加赛" if m['is_playoff'] else ("联赛末轮" if m['is_last_round'] else "常规"),
            "is_home_life_death": False,
            "physical_direction": "home", "lambda_diff": 0, "predicted_direction": "home",
            "away_xg_missing": m['away_xg'] is None,
            "home_goals": m['home_goals'], "home_goals_conceded": m['home_goals_conceded'],
            "away_goals": m['away_goals'], "away_goals_conceded": m['away_goals_conceded']
        })
    return {"matches": result}


def build_match_info(matches):
    result = []
    for m in matches:
        result.append({
            "id": m['id'], "home": m['home'], "away": m['away'],
            "event": m['event'], "time": m['time'],
            "sp_home": m['sp_home'], "sp_draw": m['sp_draw'], "sp_away": m['sp_away'],
            "asian_handicap": m['asian_handicap'], "handicap_change": m['handicap_change'],
            "match_type": "附加赛" if m['is_playoff'] else ("联赛末轮" if m['is_last_round'] else "常规"),
            "is_home_life_death": False,
            "lambda_diff": 0, "physical_direction": "home", "predicted_direction": "home",
            "h2h_missing": False, "xg_last3_missing": False,
            "xg_season_missing": m['home_xg'] is None, "roster_missing": False,
            "injury_home_missing": False, "injury_away_missing": False,
            "injury_source_unreliable": False,
            "no_coach_statement": not bool(m['coach_statement']),
            "motivation_ambiguous": False, "multi_team_linkage": False,
            "away_xg_missing": m['away_xg'] is None,
            "home_goals": m['home_goals'], "home_goals_conceded": m['home_goals_conceded'],
            "away_goals": m['away_goals'], "away_goals_conceded": m['away_goals_conceded']
        })
    return {"matches": result}


def main(text):
    matches_raw = extract_matches(text)
    matches = [parse_single_match(mid, content) for mid, content in matches_raw]
    return {
        'locked_data': build_locked_data(matches),
        'factor_params': None,
        'match_info': build_match_info(matches)
    }