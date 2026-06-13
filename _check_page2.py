import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1366, "height": 768})
        await page.goto("http://localhost:5020/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Check the analysis section after full render
        analysis = await page.query_selector("#analysisInner")
        if analysis:
            html = await analysis.inner_html()
            # Check all date groups
            import re
            for dk in ["6月12日", "6月13日", "6月14日", "6月15日", "6月16日"]:
                idx = html.find(dk)
                if idx < 0:
                    print(f"{dk}: not found")
                    continue
                ctx = html[max(0,idx-150):idx+100]
                arrow_m = re.search(r'ana-date-arrow[^>]*>([^<]+)', ctx)
                body_m = re.search(r'ana-date-body([^>]*)>', ctx)
                arrow = arrow_m.group(1) if arrow_m else "?"
                body_attr = body_m.group(1) if body_m else ""
                hidden = "display:none" in body_attr
                print(f"{dk}: arrow={arrow} hidden={hidden}")
        else:
            print("analysisInner not found")
        await browser.close()

asyncio.run(main())