import asyncio, json, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width":1280,"height":900}, user_agent="Mozilla/5.0")
        page = await ctx.new_page()
        
        # Visit SofaScore to get session cookies
        await page.goto("https://www.sofascore.com/", timeout=20000, wait_until="domcontentloaded")
        await asyncio.sleep(3)

        # Search for 川崎前锋 (Kawasaki Frontale)
        data = await page.evaluate("""async()=>{
            var r = await fetch("https://api.sofascore.com/api/v1/search/teams?q=kawasaki+frontale");
            var t = await r.text();
            return t;
        }""")
        result = json.loads(data)
        print("Kawasaki search:")
        for item in result.get("results", [])[:5]:
            ent = item.get("entity", {})
            print(f"  ID={ent.get('id')} Name={ent.get('name')} Sport={ent.get('sport',{}).get('slug')}")
        
        # Search for 广岛三箭 (Sanfrecce Hiroshima)
        data2 = await page.evaluate("""async()=>{
            var r = await fetch("https://api.sofascore.com/api/v1/search/teams?q=sanfrecce+hiroshima");
            var t = await r.text();
            return t;
        }""")
        result2 = json.loads(data2)
        print("\nHiroshima search:")
        for item in result2.get("results", [])[:5]:
            ent = item.get("entity", {})
            print(f"  ID={ent.get('id')} Name={ent.get('name')} Sport={ent.get('sport',{}).get('slug')}")
        
        await browser.close()

asyncio.run(main())
