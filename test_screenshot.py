import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        await page.goto('http://127.0.0.1:5020/', wait_until='networkidle')
        await page.wait_for_timeout(2000)
        
        cards = await page.query_selector_all('.card')
        print(f'Card count: {len(cards)}')
        
        today = await page.query_selector('#todayMatches')
        if today:
            html = await today.inner_html()
            print(f'todayMatches HTML length: {len(html)}')
            print(f'Contains card: {"card" in html}')
        else:
            print('todayMatches NOT FOUND')
        
        await page.screenshot(path=r'D:\V3.3.3-Core\screenshot_test.png', full_page=True)
        
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        await page.wait_for_timeout(500)
        if errors:
            print(f'Errors: {errors}')
        else:
            print('No page errors')
        
        await browser.close()

asyncio.run(main())
