import json, os, datetime, requests

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "odds_history", "odds_history.json")
JCZQ_URL = "https://webapi.sporttery.cn/gateway/uniform/football/getMatchCalculatorV1.qry?channel=c&poolCode=hhad,had,ttg,crs,hafu"
MAIN_URL = "https://www.sporttery.cn/"

BROWSER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}
API = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Origin": "https://www.sporttery.cn",
    "Referer": "https://www.sporttery.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}

import time as _time

def fetch():
    """Fetch from 竞彩网 with retry on failure."""
    for attempt in range(3):
        try:
            s = requests.Session()
            s.headers.update(BROWSER)
            s.get(MAIN_URL, timeout=15)
            r = s.get(JCZQ_URL, headers=API, timeout=15)
            if r.status_code == 200:
                r.encoding = "utf-8"
                return r.json()
            else:
                print('[Fetch] HTTP %d, will retry...' % r.status_code)
        except Exception as e:
            print('[Fetch] Attempt %d failed: %s' % (attempt+1, e))
        _time.sleep(3 * (attempt + 1))
    raise Exception('Failed to fetch 竞彩网 data after 3 attempts')

def snapshot(m, ts):
    o = {"ts": ts}
    for pool, keys in [("had",["h","d","a"]),("hhad",["h","d","a","goalLine"])]:
        p = m.get(pool,{})
        if not p.get("h"): continue
        d = {}
        for k in keys:
            if k == "goalLine":
                try: d[k] = float(p.get("goalLine","0") or "0")
                except: d[k]=0
            elif p.get(k):
                try: d[k]=float(p[k])
                except: pass
        if d: o[pool]=d
    for pool, keys in [("hafu",["hh","hd","ha","dh","dd","da","ah","ad","aa"]),("ttg",["s0","s1","s2","s3","s4","s5","s6","s7"])]:
        p = m.get(pool,{})
        if not p.get(keys[0]): continue
        d = {}
        for k in keys:
            if p.get(k):
                try: d[k]=float(p[k])
                except: pass
        if d: o[pool]=d
    return o

def changed(cur, prev):
    if prev is None: return True
    for k,v in cur.items():
        if k=="goalLine": continue
        if v!=prev.get(k): return True
    return False

def run():
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    print("[Track] " + ts + " Fetching...")
    data = fetch()
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    history = {}
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE,"r",encoding="utf-8") as f:
            history = json.load(f)
    new_n,upd_n = 0,0
    for day in data["value"]["matchInfoList"]:
        for m in day.get("subMatchList",[]):
            mid=str(m.get("matchId",""))
            if not mid: continue
            s=snapshot(m,ts)
            if "had" not in s and "hhad" not in s: continue
            if mid not in history:
                history[mid]={"home":m.get("homeTeamAllName",""),"away":m.get("awayTeamAllName",""),"league":m.get("leagueAllName",""),"matchDate":m.get("matchDate",""),"matchTime":m.get("matchTime",""),"matchNum":m.get("matchNumStr",""),"matchNumShort":str(m.get("matchNum","")),"goalLine":0,"had_current":None,"tracks":{}}
                new_n+=1
            e=history[mid]
            e["home"]=m.get("homeTeamAllName","")
            e["away"]=m.get("awayTeamAllName","")
            if "had" in s: e["had_current"]={"h":s["had"]["h"],"d":s["had"]["d"],"a":s["had"]["a"]}
            if "hhad" in s: e["goalLine"]=s["hhad"].get("goalLine",e.get("goalLine",0))
            for pool in ("had","hhad","hafu","ttg"):
                if pool not in s: continue
                track=e.setdefault("tracks",{}).setdefault(pool,[])
                last=track[-1] if track else None
                last_vals={k:last[k] for k in s[pool] if k!="goalLine"} if last else None
                if changed(s[pool],last_vals):
                    rec={"ts":ts}; rec.update(s[pool]); track.append(rec); upd_n+=1
    with open(HISTORY_FILE,"w",encoding="utf-8") as f:
        json.dump(history,f,ensure_ascii=False,indent=2)
    print("[Track] Done. " + str(len(history)) + " matches, +" + str(new_n) + " new, +" + str(upd_n) + " records.")
    return len(history), new_n, upd_n

if __name__=="__main__":
    run()
