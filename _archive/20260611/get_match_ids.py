import asyncio, json, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width":1280,"height":900}, user_agent="Mozilla/5.0")
        page = await ctx.new_page()
        await page.goto("https://www.sofascore.com", timeout=30000, wait_until="domcontentloaded").__await__() if False else None
        await asyncio.sleep(3)

        # Search teams and get upcoming matches
        teams_to_search = [
            "Kawasaki Frontale", "Sanfrecce Hiroshima",
            "Belgium", "Tunisia",
            "Portugal", "Chile",
            "Romania", "Wales",
            "USA", "Germany",
            "Australia", "Switzerland",
            "Panama", "Bosnia",
            "England", "New Zealand",
            "Bolivia", "Scotland",
            "Brazil", "Egypt",
            "Venezuela", "Turkey",
            "Argentina", "Honduras",
        ]
        
        team_ids = {}
        for t in teams_to_search:
            q = t.lower().replace(" ", "+")
            data = await page.evaluate("""async(q)=>{
                var r = await fetch("https://api.sofascore.com/api/v1/search/teams?q="+q);
                var t = await r.text();
                return t;
            }""", q)
            parsed = json.loads(data)
            for item in parsed.get("results", []):
                ent = item.get("entity", {})
                if ent.get("name") == t and ent.get("sport",{}).get("slug") == "football" and ent.get("gender") == "M":
                    team_ids[t] = ent["id"]
                    print(f"  {t}: ID={ent['id']}")
                    break
            if t not in team_ids:
                print(f"  {t}: NOT FOUND")

        # For each team, find their next match to get match_id
        print("\n=== Today''s Matches ===")
        found_matches = {}
        for name, tid in team_ids.items():
            data = await page.evaluate("""async(id)=>{
                var r = await fetch("https://api.sofascore.com/api/v1/team/"+id+"/events/next/0");
                var t = await r.text();
                return t;
            }""", str(tid))
            parsed = json.loads(data)
            for ev in parsed.get("events", []):
                mid = ev.get("id")
                home = ev.get("homeTeam", {}).get("name", "")
                away = ev.get("awayTeam", {}).get("name", "")
                key = f"{home} vs {away}"
                rev_key = f"{away} vs {home}"
                if key not in found_matches and rev_key not in found_matches:
                    ts = ev.get("startTimestamp", 0)
                    from datetime import datetime as dt2
                    ds = dt2.fromtimestamp(ts).strftime("%m-%d %H:%M") if ts else "?"
                    comp = ev.get("tournament", {}).get("uniqueTournament", {}).get("name", "")
                    found_matches[key] = {"mid": mid, "time": ds, "comp": comp}
                    print(f"  {key} -> mid={mid} {ds} {comp}")

        # Save for later use
        with open(r"C:\Users\gjj\Desktop\v333\data\sofascore_matches.json", "w", encoding="utf-8") as f:
            json.dump(found_matches, f, ensure_ascii=False, indent=2)
        
        await browser.close()
        print(f"\nFound {len(found_matches)} matches")
asyncio.run(main())
