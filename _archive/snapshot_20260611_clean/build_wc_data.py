import json

# Complete schedule with user-provided data
all_matches = [
    # Group A
    {"home":"墨西哥","away":"南非","group":"A","date":"6月12日","time":"03:00","venue":"墨西哥城"},
    {"home":"韩国","away":"捷克","group":"A","date":"6月12日","time":"10:00","venue":"瓜达拉哈拉"},
    {"home":"捷克","away":"南非","group":"A","date":"6月19日","time":"00:00","venue":"亚特兰大"},
    {"home":"墨西哥","away":"韩国","group":"A","date":"6月19日","time":"09:00","venue":"瓜达拉哈拉"},
    {"home":"捷克","away":"墨西哥","group":"A","date":"6月25日","time":"09:00","venue":"墨西哥城"},
    {"home":"南非","away":"韩国","group":"A","date":"6月25日","time":"09:00","venue":"蒙特雷"},
    # Group B
    {"home":"加拿大","away":"波黑","group":"B","date":"6月13日","time":"03:00","venue":"多伦多"},
    {"home":"卡塔尔","away":"瑞士","group":"B","date":"6月14日","time":"03:00","venue":"旧金山湾区"},
    {"home":"瑞士","away":"波黑","group":"B","date":"6月19日","time":"03:00","venue":"洛杉矶"},
    {"home":"加拿大","away":"卡塔尔","group":"B","date":"6月19日","time":"06:00","venue":"温哥华"},
    {"home":"瑞士","away":"加拿大","group":"B","date":"6月25日","time":"03:00","venue":"温哥华"},
    {"home":"波黑","away":"卡塔尔","group":"B","date":"6月25日","time":"03:00","venue":"西雅图"},
    # Group C
    {"home":"巴西","away":"摩洛哥","group":"C","date":"6月14日","time":"06:00","venue":"纽约/新泽西"},
    {"home":"海地","away":"苏格兰","group":"C","date":"6月14日","time":"09:00","venue":"波士顿"},
    {"home":"苏格兰","away":"摩洛哥","group":"C","date":"6月20日","time":"06:00","venue":"波士顿"},
    {"home":"巴西","away":"海地","group":"C","date":"6月20日","time":"09:00","venue":"费城"},
    {"home":"苏格兰","away":"巴西","group":"C","date":"6月25日","time":"06:00","venue":"迈阿密"},
    {"home":"摩洛哥","away":"海地","group":"C","date":"6月25日","time":"06:00","venue":"亚特兰大"},
    # Group D
    {"home":"美国","away":"巴拉圭","group":"D","date":"6月13日","time":"09:00","venue":"洛杉矶"},
    {"home":"澳大利亚","away":"土耳其","group":"D","date":"6月14日","time":"12:00","venue":"温哥华"},
    {"home":"美国","away":"澳大利亚","group":"D","date":"6月20日","time":"03:00","venue":"西雅图"},
    {"home":"土耳其","away":"巴拉圭","group":"D","date":"6月20日","time":"12:00","venue":"蒙特雷"},
    {"home":"土耳其","away":"美国","group":"D","date":"6月26日","time":"10:00","venue":"洛杉矶"},
    {"home":"巴拉圭","away":"澳大利亚","group":"D","date":"6月26日","time":"10:00","venue":"旧金山湾区"},
    # Group E
    {"home":"德国","away":"库拉索","group":"E","date":"6月15日","time":"01:00","venue":"休斯敦"},
    {"home":"科特迪瓦","away":"厄瓜多尔","group":"E","date":"6月15日","time":"07:00","venue":"费城"},
    {"home":"德国","away":"科特迪瓦","group":"E","date":"6月21日","time":"04:00","venue":"多伦多"},
    {"home":"厄瓜多尔","away":"库拉索","group":"E","date":"6月21日","time":"08:00","venue":"堪萨斯城"},
    {"home":"厄瓜多尔","away":"德国","group":"E","date":"6月26日","time":"04:00","venue":"纽约/新泽西"},
    {"home":"库拉索","away":"科特迪瓦","group":"E","date":"6月26日","time":"04:00","venue":"费城"},
    # Group F
    {"home":"荷兰","away":"日本","group":"F","date":"6月15日","time":"04:00","venue":"达拉斯"},
    {"home":"瑞典","away":"突尼斯","group":"F","date":"6月15日","time":"10:00","venue":"蒙特雷"},
    {"home":"荷兰","away":"瑞典","group":"F","date":"6月21日","time":"01:00","venue":"休斯敦"},
    {"home":"突尼斯","away":"日本","group":"F","date":"6月21日","time":"12:00","venue":"蒙特雷"},
    {"home":"日本","away":"瑞典","group":"F","date":"6月26日","time":"07:00","venue":"达拉斯"},
    {"home":"突尼斯","away":"荷兰","group":"F","date":"6月26日","time":"07:00","venue":"堪萨斯城"},
    # Group G
    {"home":"比利时","away":"埃及","group":"G","date":"6月16日","time":"03:00","venue":"西雅图"},
    {"home":"伊朗","away":"新西兰","group":"G","date":"6月16日","time":"09:00","venue":"洛杉矶"},
    {"home":"比利时","away":"伊朗","group":"G","date":"6月22日","time":"03:00","venue":"洛杉矶"},
    {"home":"新西兰","away":"埃及","group":"G","date":"6月22日","time":"09:00","venue":"温哥华"},
    {"home":"埃及","away":"伊朗","group":"G","date":"6月27日","time":"11:00","venue":"西雅图"},
    {"home":"新西兰","away":"比利时","group":"G","date":"6月27日","time":"11:00","venue":"温哥华"},
    # Group H
    {"home":"西班牙","away":"佛得角","group":"H","date":"6月16日","time":"00:00","venue":"亚特兰大"},
    {"home":"沙特阿拉伯","away":"乌拉圭","group":"H","date":"6月16日","time":"06:00","venue":"迈阿密"},
    {"home":"西班牙","away":"沙特阿拉伯","group":"H","date":"6月22日","time":"00:00","venue":"亚特兰大"},
    {"home":"乌拉圭","away":"佛得角","group":"H","date":"6月22日","time":"06:00","venue":"迈阿密"},
    {"home":"佛得角","away":"沙特阿拉伯","group":"H","date":"6月27日","time":"08:00","venue":"亚特兰大"},
    {"home":"乌拉圭","away":"西班牙","group":"H","date":"6月27日","time":"08:00","venue":"迈阿密"},
    # Group I
    {"home":"法国","away":"塞内加尔","group":"I","date":"6月17日","time":"03:00","venue":"纽约/新泽西"},
    {"home":"伊拉克","away":"挪威","group":"I","date":"6月17日","time":"06:00","venue":"波士顿"},
    {"home":"法国","away":"伊拉克","group":"I","date":"6月23日","time":"05:00","venue":"费城"},
    {"home":"挪威","away":"塞内加尔","group":"I","date":"6月23日","time":"08:00","venue":"纽约/新泽西"},
    {"home":"挪威","away":"法国","group":"I","date":"6月27日","time":"03:00","venue":"波士顿"},
    {"home":"塞内加尔","away":"伊拉克","group":"I","date":"6月27日","time":"03:00","venue":"费城"},
    # Group J
    {"home":"阿根廷","away":"阿尔及利亚","group":"J","date":"6月17日","time":"09:00","venue":"堪萨斯城"},
    {"home":"奥地利","away":"约旦","group":"J","date":"6月17日","time":"12:00","venue":"旧金山湾区"},
    {"home":"阿根廷","away":"奥地利","group":"J","date":"6月23日","time":"01:00","venue":"达拉斯"},
    {"home":"约旦","away":"阿尔及利亚","group":"J","date":"6月23日","time":"11:00","venue":"堪萨斯城"},
    {"home":"阿尔及利亚","away":"奥地利","group":"J","date":"6月28日","time":"10:00","venue":"堪萨斯城"},
    {"home":"约旦","away":"阿根廷","group":"J","date":"6月28日","time":"10:00","venue":"旧金山湾区"},
    # Group K
    {"home":"葡萄牙","away":"刚果(金)","group":"K","date":"6月18日","time":"01:00","venue":"休斯敦"},
    {"home":"乌兹别克斯坦","away":"哥伦比亚","group":"K","date":"6月18日","time":"10:00","venue":"墨西哥城"},
    {"home":"葡萄牙","away":"乌兹别克斯坦","group":"K","date":"6月24日","time":"01:00","venue":"休斯敦"},
    {"home":"哥伦比亚","away":"刚果(金)","group":"K","date":"6月24日","time":"10:00","venue":"墨西哥城"},
    {"home":"哥伦比亚","away":"葡萄牙","group":"K","date":"6月28日","time":"07:30","venue":"迈阿密"},
    {"home":"刚果(金)","away":"乌兹别克斯坦","group":"K","date":"6月28日","time":"07:30","venue":"亚特兰大"},
    # Group L
    {"home":"英格兰","away":"克罗地亚","group":"L","date":"6月18日","time":"04:00","venue":"达拉斯"},
    {"home":"加纳","away":"巴拿马","group":"L","date":"6月18日","time":"07:00","venue":"多伦多"},
    {"home":"英格兰","away":"加纳","group":"L","date":"6月24日","time":"04:00","venue":"波士顿"},
    {"home":"巴拿马","away":"克罗地亚","group":"L","date":"6月24日","time":"07:00","venue":"多伦多"},
    {"home":"巴拿马","away":"英格兰","group":"L","date":"6月28日","time":"03:00","venue":"纽约/新泽西"},
    {"home":"克罗地亚","away":"加纳","group":"L","date":"6月28日","time":"03:00","venue":"费城"},
]

# Build groups
group_teams = {}
for m in all_matches:
    g = m["group"]
    if g not in group_teams: group_teams[g] = set()
    group_teams[g].add((m["home"], m["home"]))  # placeholder
    group_teams[g].add(m["home"])
    group_teams[g].add(m["away"])

# Country flags
country_flags = {
    "墨西哥":"🇲🇽","南非":"🇿🇦","韩国":"🇰🇷","捷克":"🇨🇿",
    "加拿大":"🇨🇦","波黑":"🇧🇦","瑞士":"🇨🇭","卡塔尔":"🇶🇦",
    "巴西":"🇧🇷","摩洛哥":"🇲🇦","海地":"🇭🇹","苏格兰":"🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "美国":"🇺🇸","巴拉圭":"🇵🇾","澳大利亚":"🇦🇺","土耳其":"🇹🇷",
    "德国":"🇩🇪","库拉索":"🇨🇼","科特迪瓦":"🇨🇮","厄瓜多尔":"🇪🇨",
    "荷兰":"🇳🇱","日本":"🇯🇵","瑞典":"🇸🇪","突尼斯":"🇹🇳",
    "比利时":"🇧🇪","埃及":"🇪🇬","伊朗":"🇮🇷","新西兰":"🇳🇿",
    "西班牙":"🇪🇸","佛得角":"🇨🇻","沙特阿拉伯":"🇸🇦","乌拉圭":"🇺🇾",
    "法国":"🇫🇷","塞内加尔":"🇸🇳","伊拉克":"🇮🇶","挪威":"🇳🇴",
    "阿根廷":"🇦🇷","阿尔及利亚":"🇩🇿","奥地利":"🇦🇹","约旦":"🇯🇴",
    "葡萄牙":"🇵🇹","刚果(金)":"🇨🇩","乌兹别克斯坦":"🇺🇿","哥伦比亚":"🇨🇴",
    "英格兰":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","克罗地亚":"🇭🇷","加纳":"🇬🇭","巴拿马":"🇵🇦",
}

# Merge with JCZQ odds
with open("D:/V3.3.3-Core/data/raw_jczq.json","r",encoding="utf-8") as f:
    jczq = json.load(f)

# Build JCZQ lookup
jczq_lookup = {}
for day in jczq["value"]["matchInfoList"]:
    for m in day["subMatchList"]:
        if m.get("leagueAllName","") != "世界杯": continue
        home = m.get("homeTeamAllName","")
        away = m.get("awayTeamAllName","")
        date = m.get("matchDate","")
        had = m.get("had",{})
        hhad = m.get("hhad",{})
        key = home + "|" + away + "|" + date
        jczq_lookup[key] = {
            "id": m.get("matchNumStr",""),
            "sp_h": had.get("h","-"), "sp_d": had.get("d","-"), "sp_a": had.get("a","-"),
            "hh_h": hhad.get("h","-"), "hh_d": hhad.get("d","-"), "hh_a": hhad.get("a","-"),
            "handicap": m.get("goalLine", 0),
        }

# Finalize matches with odds + flags
final_matches = []
match_odds_count = 0
for m in all_matches:
    # Normalize team name for JCZQ lookup
    home_jczq = "刚果(金)" if m["home"] == "刚果(金)" else m["home"]
    away_jczq = "刚果(金)" if m["away"] == "刚果(金)" else m["away"]
    
    # Calculate date_ymd
    import re
    dm = re.search(r"(\d+)月(\d+)日", m["date"])
    month, day = int(dm.group(1)), int(dm.group(2))
    ymd = f"2026-{month:02d}-{day:02d}"
    
    # Find odds
    key = home_jczq + "|" + away_jczq + "|" + ymd
    odds = jczq_lookup.get(key)
    if odds:
        match_odds_count += 1
    
    # Determine round
    # R1: June 12-18, R2: June 19-24, R3: June 25-28
    if day <= 18: rnd = 1
    elif day <= 24: rnd = 2
    else: rnd = 3
    
    final_matches.append({
        "home": m["home"], "away": m["away"],
        "group": m["group"], "round": rnd,
        "date": m["date"], "time": m["time"],
        "venue": m["venue"],
        "home_flag": country_flags.get(m["home"], ""),
        "away_flag": country_flags.get(m["away"], ""),
        "odds": odds,
    })

# Build groups dict
groups_dict = {}
for m in final_matches:
    g = m["group"]
    if g not in groups_dict: groups_dict[g] = set()
    groups_dict[g].add(m["home"])
    groups_dict[g].add(m["away"])

output = {
    "matches": final_matches,
    "groups": {g: sorted(t) for g, t in groups_dict.items()},
    "match_count": len(final_matches),
    "odds_count": match_odds_count,
}

with open("D:/V3.3.3-Core/data/wc_schedule.json","w",encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Total: {len(final_matches)} matches")
print(f"With odds: {match_odds_count}")
print(f"Groups: {sorted(groups_dict.keys())}")
for g in sorted(groups_dict.keys()):
    print(f"  {g}: {', '.join(sorted(groups_dict[g]))}")
