import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1366, "height": 768})
        
        all_console = []
        page.on("console", lambda msg: all_console.append(f"[{msg.type}] {msg.text}"))
        
        await page.goto("http://localhost:5020/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(5000)
        
        print("=== CONSOLE LOGS ===")
        for log in all_console:
            print(log)
        
        print("\n=== WC_MATCHES_DATA check ===")
        result = await page.evaluate("typeof WC_MATCHES_DATA !== 'undefined' ? WC_MATCHES_DATA.length : 'UNDEFINED'")
        print("WC_MATCHES_DATA:", result)
        
        await browser.close()

asyncio.run(main())