import asyncio, json, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width":1280,"height":900}, user_agent="Mozilla/5.0")
        page = await ctx.new_page()
        await asyncio.sleep(2)

        # All team IDs from previous search
        teams = {
            "Kawasaki Frontale": 5127, "Sanfrecce Hiroshima": 3135,
            "Belgium": 4717, "Tunisia": 4729,
            "Portugal": 4704, "Chile": 4754,
            "Romania": 4477, "Wales": 4702,
            "USA": 4724, "Germany": 4711,
            "Australia": 4741, "Switzerland": 4699,
            "Panama": 5164, "Bosnia & Herzegovina": None,
            "England": 4713, "New Zealand": 4784,
            "Bolivia": 4746, "Scotland": 4695,
            "Brazil": 4748, "Egypt": 4758,
            "Venezuela": 4722, "Türkiye": None,
            "Argentina": 4819, "Honduras": 4827,
        }
        
        # Search for missing teams
        for t in ["Bosnia", "Turkey"]:
            data = await page.evaluate("""async(q)=>{
                var r = await fetch("https://api.sofascore.com/api/v1/search/teams?q="+q);
                return await r.text();
            }""", t.lower())
            parsed = json.loads(data)
            for item in parsed.get("results", []):
                ent = item.get("entity", {})
                if ent.get("sport",{}).get("slug") == "football" and ent.get("gender") == "M":
                    print(f"  {t}: {ent.get('name')} ID={ent.get('id')}")
        print()

        # Get recent 5 for each team (show key data)
        for name, tid in teams.items():
            if not tid:
                continue
            data = await page.evaluate("""async(id)=>{
                var r = await fetch("https://api.sofascore.com/api/v1/team/"+id+"/events/last/0");
                return await r.text();
            }""", str(tid))
            events = json.loads(data).get("events", [])
            print(f"\n=== {name} ===")
            for ev in events[:5]:
                ts = ev.get("startTimestamp", 0)
                from datetime import datetime as dt
                ds = dt.fromtimestamp(ts).strftime("%m-%d") if ts else "?"
                home = ev.get("homeTeam", {}).get("name", "")
                away = ev.get("awayTeam", {}).get("name", "")
                hs = ev.get("homeScore", {}).get("current", "")
                asc = ev.get("awayScore", {}).get("current", "")
                comp = ev.get("tournament", {}).get("uniqueTournament", {}).get("name", "")
                status = ev.get("status", {}).get("type", "")
                print(f"  {ds}  {home} vs {away}  {hs}-{asc}  [{comp}]")
        
        await browser.close()

asyncio.run(main())
