import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        
        await page.goto('http://127.0.0.1:5000/')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)
        
        # Check if renderCalendarView exists and call it
        has_render = await page.evaluate('typeof renderCalendarView === "function"')
        print('renderCalendarView exists:', has_render)
        
        if has_render:
            await page.evaluate('renderCalendarView()')
            await asyncio.sleep(2)
            await page.screenshot(path='D:/V3.3.3-Core/calendar_result.png', full_page=True)
            print('Calendar screenshot saved')
        
        await browser.close()

asyncio.run(main())
