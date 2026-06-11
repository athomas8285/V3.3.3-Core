import asyncio, json, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width":1280,"height":900}, user_agent="Mozilla/5.0")
        page = await ctx.new_page()
        
        print("Visiting SofaScore...")
        try:
            await page.goto("https://www.sofascore.com", timeout=60000, wait_until="domcontentloaded")
            await asyncio.sleep(5)
            print("Page loaded!")
        except:
            print("Page load timeout, trying API directly...")
        
        # Try API endpoints
        endpoints = [
            "https://api.sofascore.com/api/v1/search/teams?q=kawasaki",
            "https://api.sofascore.com/api/v1/unique-tournament/405",  # J-League
        ]
        
        for ep in endpoints:
            data = await page.evaluate("""async(url)=>{
                try {
                    var r = await fetch(url, {headers: {"Accept": "application/json"}});
                    return JSON.stringify({status: r.status, body: (await r.text()).substring(0, 3000)});
                } catch(e) { return JSON.stringify({status: "error", body: e.message}); }
            }""", ep)
            result = json.loads(data)
            label = ep.split(".com")[1] if ".com" in ep else ep
            print(f"[{result['status']}] {label}")
            if result["status"] == 200:
                print(f"  {result['body'][:500]}")
        
        await browser.close()

asyncio.run(main())
