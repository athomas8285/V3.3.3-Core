import requests, json
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Referer': 'https://www.sporttery.cn/'}
url = 'https://webapi.sporttery.cn/gateway/uniform/football/getMatchCalculatorV1.qry?channel=c&poolCode=hhad,had,ttg,crs,hafu'
resp = requests.get(url, headers=headers, timeout=15)
data = resp.json()
m = data['value']['matchInfoList'][0]['subMatchList'][0]

print('=== ttg (Total Goals) ===')
ttg = m['ttg']
for k in ['s0','s1','s2','s3','s4','s5','s6','s7']:
    print(f'  {k}: {ttg.get(k)}')

print()
print('=== crs (Correct Score) first 15 ===')
crs = m['crs']
score_keys = sorted([k for k in crs.keys() if k.startswith('s')])
for k in score_keys[:15]:
    print(f'  {k}: {crs[k]}')
print(f'  Total CRS keys: {len(score_keys)}')

print()
print('=== hafu (Half Full) ===')
hafu = m['hafu']
for k in ['hh','hd','ha','dh','dd','da','ah','ad','aa']:
    print(f'  {k}: {hafu.get(k)}')
