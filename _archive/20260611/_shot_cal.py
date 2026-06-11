import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        
        await page.goto('http://127.0.0.1:5000/')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        
        await page.screenshot(path='D:/V3.3.3-Core/calendar_before.png', full_page=True)
        print('Screenshot 1 saved')
        
        # Click calendar nav item
        cal_items = await page.query_selector_all('.wc-sub-item')
        print(f'WC items: {len(cal_items)}')
        
        for item in cal_items:
            text = await item.inner_text()
            print(f'  Item: [{text}]')
        
        # Try clicking the calendar item directly via JS
        has_render = await page.evaluate('typeof renderCalendarView === "function"')
        print(f'renderCalendarView exists: {has_render}')
        
        if has_render:
            await page.evaluate('renderCalendarView()')
            await asyncio.sleep(1)
            await page.screenshot(path='D:/V3.3.3-Core/calendar_after.png', full_page=True)
            print('Calendar screenshot saved')
        
        # Get page HTML to verify
        html = await page.content()
        with open('D:/V3.3.3-Core/calendar_dump.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Page HTML saved: {len(html)} bytes')
        
        await browser.close()

asyncio.run(main())
