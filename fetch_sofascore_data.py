import asyncio, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEAM_NAME_MAP = {
    "墨西哥": "Mexico", "南非": "South Africa", "韩国": "Korea Republic",
    "捷克": "Czech Republic", "加拿大": "Canada", "波黑": "Bosnia and Herzegovina",
    "美国": "USA", "巴拉圭": "Paraguay", "卡塔尔": "Qatar",
    "瑞士": "Switzerland", "巴西": "Brazil", "摩洛哥": "Morocco",
    "海地": "Haiti", "苏格兰": "Scotland", "澳大利亚": "Australia",
    "土耳其": "Turkiye", "德国": "Germany", "库拉索": "Curacao",
    "荷兰": "Netherlands", "日本": "Japan", "科特迪瓦": "Ivory Coast",
    "厄瓜多尔": "Ecuador", "瑞典": "Sweden", "突尼斯": "Tunisia",
    "西班牙": "Spain", "佛得角": "Cape Verde", "比利时": "Belgium",
    "埃及": "Egypt", "沙特阿拉伯": "Saudi Arabia", "乌拉圭": "Uruguay",
    "伊朗": "Iran", "新西兰": "New Zealand", "法国": "France",
    "塞内加尔": "Senegal", "伊拉克": "Iraq", "挪威": "Norway",
    "阿根廷": "Argentina", "阿尔及利亚": "Algeria", "奥地利": "Austria",
    "约旦": "Jordan", "葡萄牙": "Portugal", "刚果(金)": "DR Congo",
    "刚果金": "DR Congo", "英格兰": "England", "克罗地亚": "Croatia",
    "加纳": "Ghana", "巴拿马": "Panama", "乌兹别克斯坦": "Uzbekistan",
    "哥伦比亚": "Colombia",
}

def load_json(filename):
    path = os.path.join(BASE_DIR, 'data', filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(data, filename):
    path = os.path.join(BASE_DIR, 'data', filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'  -> {path}')

async def fetch_json(page, url):
    js = '''async(url)=>{
        var r = await fetch(url);
        var t = await r.text();
        return JSON.stringify({s:r.status, b:t.substring(0,100000)});
    }'''
    data = await page.evaluate(js, url)
    result = json.loads(data)
    if result.get('s') == 200:
        return json.loads(result['b'])
    return {}

async def main():
    locked = load_json('locked_data.json')
    matches = locked.get('matches', [])
    if not matches:
        print('[ERROR] No matches')
        return

    team_ids = load_json('sofascore_team_ids.json')
    sofa_data = {}
    stats = {'teams': len(team_ids), 'matches_found': 0}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={'width':1280,'height':900},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
        page = await ctx.new_page()
        try:
            await page.goto('https://www.sofascore.com/', timeout=15000, wait_until='domcontentloaded')
            await asyncio.sleep(2)
        except Exception as e:
            print(f'[WARN] Page: {e}')

        for i, m in enumerate(matches):
            mid = m.get('id', f'match_{i}')
            hcn = m.get('home', ''); acn = m.get('away', '')
            hen = TEAM_NAME_MAP.get(hcn, hcn); aen = TEAM_NAME_MAP.get(acn, acn)
            print(f'[{i+1}/{len(matches)}] {hcn} vs {acn}')
            md = {'home':hcn, 'away':acn, 'ts': datetime.now().isoformat()}

            # Get team IDs
            hid = team_ids.get(hcn); aid = team_ids.get(acn)
            if not hid:
                sr = await fetch_json(page, f'https://api.sofascore.com/api/v1/search/teams?q={hen}')
                for item in sr.get('results', []):
                    e = item.get('entity', {})
                    if e.get('sport',{}).get('slug')=='football' and e.get('national') and e.get('gender')=='M':
                        hid = e['id']; team_ids[hcn]=hid; stats['teams']+=1; break
            if not aid:
                sr = await fetch_json(page, f'https://api.sofascore.com/api/v1/search/teams?q={aen}')
                for item in sr.get('results', []):
                    e = item.get('entity', {})
                    if e.get('sport',{}).get('slug')=='football' and e.get('national') and e.get('gender')=='M':
                        aid = e['id']; team_ids[acn]=aid; stats['teams']+=1; break
            save_json(team_ids, 'sofascore_team_ids.json')

            if not hid and not aid:
                sofa_data[mid]=md; continue

            # Find match event ID from upcoming events
            eid = None
            seen = set()
            for tid, ten, aen_local in [(hid, hen, aen), (aid, aen, hen)]:
                if not tid: continue
                evs = await fetch_json(page, f'https://api.sofascore.com/api/v1/team/{tid}/events/next/0')
                for ev in evs.get('events', []):
                    ev_id = ev.get('id')
                    if ev_id in seen: continue
                    seen.add(ev_id)
                    h = ev.get('homeTeam',{}).get('name','').lower()
                    a = ev.get('awayTeam',{}).get('name','').lower()
                    if aen_local.lower() in [h, a] or ten.lower() in [h, a]:
                        eid=ev_id; md['event_id']=eid; stats['matches_found']+=1; break
                if eid: break

            if not eid:
                print(f'  [WARN] No SofaScore event found'); sofa_data[mid]=md; continue

            # Fetch match data
            detail = await fetch_json(page, f'https://api.sofascore.com/api/v1/event/{eid}')
            if detail:
                ev = detail.get('event',{})
                md['venue'] = ev.get('venue',{})
                md['start_time'] = ev.get('startTimestamp')
                md['status'] = ev.get('status',{}).get('type')

            # Lineups / missing
            lu = await fetch_json(page, f'https://api.sofascore.com/api/v1/event/{eid}/lineups')
            if lu:
                for sk in ['home','away']:
                    mp = lu.get(sk,{}).get('missingPlayers',[])
                    md[f'missing_{sk}'] = [{'name':p.get('player',{}).get('name'),
                        'pos':p.get('player',{}).get('position'),'reason':p.get('description')} for p in mp]

            # H2H
            h2h = await fetch_json(page, f'https://api.sofascore.com/api/v1/event/{eid}/h2h')
            if h2h:
                md['h2h'] = []
                for ev in h2h.get('events',[])[:5]:
                    ts = ev.get('startTimestamp',0)
                    md['h2h'].append({'date':datetime.fromtimestamp(ts).strftime('%Y-%m-%d') if ts else None,
                        'home':ev.get('homeTeam',{}).get('name'),'away':ev.get('awayTeam',{}).get('name'),
                        'score':f"{ev.get('homeScore',{}).get('display',0)}-{ev.get('awayScore',{}).get('display',0)}"})

            # Recent xG for both teams
            for sl, tid, ten in [('home',hid,hen),('away',aid,aen)]:
                if not tid: continue
                recent = await fetch_json(page, f'https://api.sofascore.com/api/v1/team/{tid}/events/last/0')
                rxg = []; cnt=0
                for ev in recent.get('events',[]):
                    if cnt>=3: break
                    if ev.get('id')==eid: continue
                    st = ev.get('status',{}).get('type','')
                    if st not in ('finished','finished_after_penalties','finished_after_extra_time'): continue
                    ts = ev.get('startTimestamp',0)
                    sd = await fetch_json(page, f'https://api.sofascore.com/api/v1/match/{ev["id"]}/statistics')
                    xgh,xga=None,None
                    for period in sd.get('statistics',[]):
                        for g in period.get('groups',[]):
                            for item in g.get('statisticsItems',[]):
                                if 'xG' in item.get('name','') or 'expected' in item.get('name','').lower():
                                    try: xgh=float(item.get('home',0)); xga=float(item.get('away',0))
                                    except: pass
                    is_h = ev.get('homeTeam',{}).get('name','').lower()==ten.lower()
                    rxg.append({'date':datetime.fromtimestamp(ts).strftime('%Y-%m-%d') if ts else None,
                        'home':ev.get('homeTeam',{}).get('name'),'away':ev.get('awayTeam',{}).get('name'),
                        'score':f"{ev.get('homeScore',{}).get('display',0)}-{ev.get('awayScore',{}).get('display',0)}",
                        'xg_for':xgh if is_h else xga,'xg_against':xga if is_h else xgh})
                    cnt+=1
                md[f'xg_{sl}']=rxg

            sofa_data[mid]=md
            save_json(sofa_data, 'sofascore_data.json')
            await asyncio.sleep(0.3)

    save_json(team_ids, 'sofascore_team_ids.json')
    print(f'Done. Teams:{stats["teams"]}, Matches:{stats["matches_found"]}')

if __name__ == '__main__':
    asyncio.run(main())
