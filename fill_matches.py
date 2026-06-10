import json
with open("D:/V3.3.3-Core/data/wc_schedule.json","r",encoding="utf-8") as f:
    d = json.load(f)

# Build per-group team lists
groups = d["groups"]
# Convert to lists
group_teams = {g: sorted(teams) for g, teams in groups.items()}

# For each group, figure out what matches are missing
# Each group of 4 teams should have 6 matches
# Round 1: T1 vs T2, T3 vs T4
# Round 2: T1 vs T3, T2 vs T4  
# Round 3: T1 vs T4, T2 vs T3

# Build set of existing matches
existing = set()
for m in d["matches"]:
    # Sort teams for dedup
    pair = tuple(sorted([m["home"], m["away"]]))
    existing.add(pair)

# Get the last date per group to figure out round 3 dates
# We need to assign round 3 dates (one match per day, staggered across groups)
from collections import defaultdict

# First figure out what dates each group's existing matches fall on
group_dates = defaultdict(list)
for m in d["matches"]:
    group_dates[m["group"]].append(m["date"])

# Generate missing matches
new_matches = []
for g in sorted(group_teams.keys()):
    teams = group_teams[g]
    n = len(teams)
    # All possible pairings
    all_pairs = []
    for i in range(n):
        for j in range(i+1, n):
            all_pairs.append((teams[i], teams[j]))
    
    missing = [p for p in all_pairs if tuple(sorted(p)) not in existing]
    
    if missing:
        # Assign round 3 dates
        # Groups A-H play round 3 on June 23-24
        # Groups I-L play round 3 on June 24-25
        # We need 2 match dates per group (2 matches per round)
        base_date = 23 if g <= "H" else 24
        # Assign dates based on group order
        group_idx = ord(g) - ord("A")
        date_offset = group_idx // 4  # 4 groups per day
        r3_date1 = f"6月{base_date + date_offset}日"
        r3_date2 = f"6月{base_date + date_offset + 1}日"
        
        for idx, (t1, t2) in enumerate(missing):
            # Figure out home/away (can be arbitrary, use alphabetical)
            home, away = t1, t2
            match_date = r3_date1 if idx == 0 else r3_date2
            new_matches.append({
                "home": home, "away": away, "group": g,
                "date": match_date,
                "time": "待定",
                "date_ymd": "",
                "odds": None,
                "home_flag": "", "away_flag": ""
            })

# Add missing matches
d["matches"].extend(new_matches)
d["match_count"] = len(d["matches"])

# Re-sort by group and date
group_order = {g: i for i, g in enumerate(sorted(set(m["group"] for m in d["matches"])))}
d["matches"].sort(key=lambda m: (group_order.get(m["group"], 99), m.get("date", "")))

with open("D:/V3.3.3-Core/data/wc_schedule.json","w",encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

# Verify
from collections import Counter
gc = Counter(m["group"] for m in d["matches"])
total = len(d["matches"])
print(f"Total matches: {total} (should be 72)")

for g in sorted(gc.keys()):
    print(f"  {g}: {gc[g]} matches (should be 6)")
    # Show the matches
    ms = [m for m in d["matches"] if m["group"] == g]
    for m in ms:
        print(f"    {m['date']} {m['time']} {m['home']} vs {m['away']}")
    print()
