import json

with open("D:/V3.3.3-Core/data/wc_schedule.json","r",encoding="utf-8") as f:
    wc = json.load(f)

with open("D:/V3.3.3-Core/data/raw_jczq.json","r",encoding="utf-8") as f:
    jczq = json.load(f)

# Team name fix
team_fix = {"刚果金": "刚果(金)"}

jczq_matches = {}
for day in jczq["value"]["matchInfoList"]:
    for m in day["subMatchList"]:
        if m.get("leagueAllName","") != "世界杯":
            continue
        home = m.get("homeTeamAllName","")
        away = m.get("awayTeamAllName","")
        date_str = m.get("matchDate","")
        time_str = m.get("matchTime","")[:5]
        
        had = m.get("had", {})
        hhad = m.get("hhad", {})
        
        key = home + "|" + away + "|" + date_str
        jczq_matches[key] = {
            "id": m.get("matchNumStr",""),
            "datetime": date_str + " " + time_str,
            "sp_h": had.get("h","-"), "sp_d": had.get("d","-"), "sp_a": had.get("a","-"),
            "hh_h": hhad.get("h","-"), "hh_d": hhad.get("d","-"), "hh_a": hhad.get("a","-"),
            "handicap": m.get("goalLine", 0),
        }

# Match schedule with odds
import re
matched_count = 0
for m in wc["matches"]:
    home = m["home"]
    away = m["away"]
    # Fix team name if needed
    if home in team_fix: home = team_fix[home]
    if away in team_fix: away = team_fix[away]
    
    dm = re.search(r"(\d+)月(\d+)日", m["date"])
    ymd = f"2026-{int(dm.group(1)):02d}-{int(dm.group(2)):02d}" if dm else m["date"]
    
    key = home + "|" + away + "|" + ymd
    odds = jczq_matches.get(key)
    
    # Also try with original names
    if not odds:
        key2 = m["home"] + "|" + m["away"] + "|" + ymd
        odds = jczq_matches.get(key2)
    
    if odds:
        m["odds"] = odds
        matched_count += 1
    else:
        m["odds"] = None

# Add team flags mapping
country_flags = {
    "墨西哥": "🇲🇽", "南非": "🇿🇦", "韩国": "🇰🇷", "捷克": "🇨🇿",
    "加拿大": "🇨🇦", "波黑": "🇧🇦", "瑞士": "🇨🇭",
    "美国": "🇺🇸", "巴拉圭": "🇵🇾",
    "卡塔尔": "🇶🇦", "巴西": "🇧🇷", "摩洛哥": "🇲🇦",
    "海地": "🇭🇹", "苏格兰": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "澳大利亚": "🇦🇺", "土耳其": "🇹🇷",
    "德国": "🇩🇪", "库拉索": "🇨🇼", "荷兰": "🇳🇱", "日本": "🇯🇵",
    "科特迪瓦": "🇨🇮", "厄瓜多尔": "🇪🇨", "瑞典": "🇸🇪", "突尼斯": "🇹🇳",
    "西班牙": "🇪🇸", "佛得角": "🇨🇻", "比利时": "🇧🇪", "埃及": "🇪🇬",
    "沙特阿拉伯": "🇸🇦", "乌拉圭": "🇺🇾", "伊朗": "🇮🇷", "新西兰": "🇳🇿",
    "法国": "🇫🇷", "塞内加尔": "🇸🇳", "伊拉克": "🇮🇶", "挪威": "🇳🇴",
    "阿根廷": "🇦🇷", "阿尔及利亚": "🇩🇿", "奥地利": "🇦🇹", "约旦": "🇯🇴",
    "葡萄牙": "🇵🇹", "刚果(金)": "🇨🇩", "刚果金": "🇨🇩",
    "英格兰": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "克罗地亚": "🇭🇷", "加纳": "🇬🇭", "巴拿马": "🇵🇦",
    "乌兹别克斯坦": "🇺🇿", "哥伦比亚": "🇨🇴",
    "意大利": "🇮🇹", "丹麦": "🇩🇰",
}

# Add flags to each match
for m in wc["matches"]:
    m["home_flag"] = country_flags.get(m["home"], "")
    m["away_flag"] = country_flags.get(m["away"], "")

wc["match_count"] = len(wc["matches"])
wc["odds_count"] = matched_count

with open("D:/V3.3.3-Core/data/wc_schedule.json","w",encoding="utf-8") as f:
    json.dump(wc, f, ensure_ascii=False, indent=2)

print(f"Total matches: {wc['match_count']}")
print(f"With odds: {wc['odds_count']}")
print(f"Groups: {sorted(wc['groups'].keys())}")
