import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://127.0.0.1:5020/", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.wait_for_timeout(500)

        # Check cards have no trace of the removed elements
        trend_spans = await page.query_selector_all(".trend")
        expand_arrows = await page.query_selector_all(".expand-arrow")
        print(f"trend spans remaining: {len(trend_spans)}")
        print(f"expand-arrow divs remaining: {len(expand_arrows)}")
        print(f"JS errors: {errors}")

        await page.screenshot(path=r"D:\V3.3.3-Core\screenshot_no_arrows.png", full_page=True)
        await browser.close()

asyncio.run(main())
