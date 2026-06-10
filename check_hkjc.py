import requests, re
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
# Try HKJC
url = "https://football.hkjc.com/football/premier/odds/comparison.aspx"
resp = requests.get(url, headers=headers, timeout=15)
print(f"HKJC: status={resp.status_code} len={len(resp.text)}")
# Check if it contains odds data
if resp.status_code == 200:
    # Look for match info in the page
    lines = resp.text.split("\n")
    for l in lines[:100]:
        if "odds" in l.lower() or "match" in l.lower() or "handicap" in l.lower():
            print(l[:200])
