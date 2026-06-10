import json, sys
sys.stdout.reconfigure(encoding="utf-8")
data = json.load(open("D:/V3.3.3-Core/data/raw_jczq.json", "r", encoding="utf-8"))
value = data.get("value",{})
match_list = value.get("matchInfoList",[])
for day in match_list:
    date = day.get("businessDate","")
    subs = day.get("subMatchList",[])
    wc = [m for m in subs if "世界杯" in (m.get("leagueAllName","") or m.get("leagueName",""))]
    if not wc:
        continue
    print(f"{date}: {len(wc)} 场世界杯")
    for m in wc:
        had = m.get("had",{})
        hhad = m.get("hhad",{})
        goal = m.get("goalLine",0)
        num = m.get("matchNumStr","?")
        home = m.get("homeTeamAllName","")
        away = m.get("awayTeamAllName","")
        print(f"  {num} {home} vs {away}")
        print(f"    SP: {had.get('h','-')} / {had.get('d','-')} / {had.get('a','-')}  让球:{goal}")
        print(f"    让SP: {hhad.get('h','-')} / {hhad.get('d','-')} / {hhad.get('a','-')}")
