import asyncio, json, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width":1280,"height":900}, user_agent="Mozilla/5.0")
        page = await ctx.new_page()
        await asyncio.sleep(2)

        # Kawasaki Frontale recent matches
        data = await page.evaluate("""async()=>{
            var r = await fetch("https://api.sofascore.com/api/v1/team/5127/events/last/0");
            return await r.text();
        }""")
        events = json.loads(data).get("events", [])
        print("=== Kawasaki Frontale Recent 5 ===")
        for ev in events[:5]:
            ts = ev.get("startTimestamp", 0)
            from datetime import datetime as dt
            ds = dt.fromtimestamp(ts).strftime("%m-%d %H:%M") if ts else "?"
            home = ev.get("homeTeam", {}).get("name", "")
            away = ev.get("awayTeam", {}).get("name", "")
            hs = ev.get("homeScore", {}).get("current", "")
            asc = ev.get("awayScore", {}).get("current", "")
            comp = ev.get("tournament", {}).get("uniqueTournament", {}).get("name", "")
            status = ev.get("status", {}).get("type", "")
            print(f"  {ds} {home} {hs}-{asc} {away} [{comp}] ({status})")

        # Hiroshima recent matches
        data2 = await page.evaluate("""async()=>{
            var r = await fetch("https://api.sofascore.com/api/v1/team/3135/events/last/0");
            return await r.text();
        }""")
        events2 = json.loads(data2).get("events", [])
        print("\n=== Sanfrecce Hiroshima Recent 5 ===")
        for ev in events2[:5]:
            ts = ev.get("startTimestamp", 0)
            from datetime import datetime as dt
            ds = dt.fromtimestamp(ts).strftime("%m-%d %H:%M") if ts else "?"
            home = ev.get("homeTeam", {}).get("name", "")
            away = ev.get("awayTeam", {}).get("name", "")
            hs = ev.get("homeScore", {}).get("current", "")
            asc = ev.get("awayScore", {}).get("current", "")
            comp = ev.get("tournament", {}).get("uniqueTournament", {}).get("name", "")
            status = ev.get("status", {}).get("type", "")
            print(f"  {ds} {home} {hs}-{asc} {away} [{comp}] ({status})")

        await browser.close()

asyncio.run(main())
