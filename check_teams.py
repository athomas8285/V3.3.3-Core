# Check team name differences between Bing and jczq
import json

with open("D:/V3.3.3-Core/data/raw_jczq.json","r",encoding="utf-8") as f:
    jczq = json.load(f)

# Get all jczq team names for WC matches
jczq_teams = set()
for day in jczq["value"]["matchInfoList"]:
    for m in day["subMatchList"]:
        if m.get("leagueAllName","") == "世界杯":
            jczq_teams.add(m.get("homeTeamAllName",""))
            jczq_teams.add(m.get("awayTeamAllName",""))

print("JCZQ team names:")
for t in sorted(jczq_teams):
    print(f"  {t}")

# Bing team names
bing_teams = set()
with open("D:/V3.3.3-Core/data/wc_schedule.json","r",encoding="utf-8") as f:
    wc = json.load(f)
for m in wc["matches"]:
    bing_teams.add(m["home"])
    bing_teams.add(m["away"])

print("\nBing team names:")
for t in sorted(bing_teams):
    print(f"  {t}")

# Compare
only_bing = bing_teams - jczq_teams
only_jczq = jczq_teams - bing_teams
print(f"\nOnly in Bing: {sorted(only_bing)}")
print(f"Only in jczq: {sorted(only_jczq)}")
