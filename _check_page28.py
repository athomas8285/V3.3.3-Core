import urllib.request, json, sys
sys.stdout.reconfigure(encoding="utf-8")
req = urllib.request.urlopen("http://localhost:5020/api/wc-matches", timeout=10)
data = json.loads(req.read().decode("utf-8"))
matches = data.get("matches", [])
print(f"Total matches: {len(matches)}")
# Print all match ids and actual_scores
for m in matches:
    result = m.get("actual_score", "N/A")
    hit = m.get("hit", "N/A")
    mid = m.get("match_id", "?")
    if result and result != "N/A":
        print(f"  {mid}: {m.get('home','?')} vs {m.get('away','?')} -> {result} hit={hit}")
    else:
        print(f"  {mid}: {m.get('home','?')} vs {m.get('away','?')} -> no result")