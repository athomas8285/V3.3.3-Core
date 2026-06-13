import urllib.request, json, sys
sys.stdout.reconfigure(encoding="utf-8")
req = urllib.request.urlopen("http://localhost:5020/api/wc-matches", timeout=10)
data = json.loads(req.read().decode("utf-8"))
matches = data.get("matches", [])
print(f"Total matches: {len(matches)}")
# Check completed matches
for m in matches:
    if m.get("actual_score"):
        print(f"  {m.get('match_id','?')}: {m.get('home','?')} vs {m.get('away','?')}")
        print(f"    actual_score={m.get('actual_score')}, direction={m.get('direction')}, hit={m.get('hit')}, half_full={m.get('half_full','NOT PRESENT')}")
        # Check all keys
        print(f"    keys: {list(m.keys())}")