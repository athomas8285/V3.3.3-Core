import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        await page.goto('http://127.0.0.1:5020/', wait_until='networkidle')
        await page.wait_for_timeout(2000)

        card = await page.query_selector('.card')
        if not card:
            print('No card found')
            await browser.close()
            return
        box = await card.bounding_box()
        print(f'Card dimensions (not expanded):')
        print(f'  width  = {box["width"]:.1f}px')
        print(f'  height = {box["height"]:.1f}px')
        print(f'  x      = {box["x"]:.1f}px')
        print(f'  y      = {box["y"]:.1f}px')

        # Also check todayMatches container width
        container = await page.query_selector('#todayMatches')
        if container:
            cbox = await container.bounding_box()
            print(f'\ntodayMatches container:')
            print(f'  width  = {cbox["width"]:.1f}px')
            print(f'  height = {cbox["height"]:.1f}px')

        await browser.close()

asyncio.run(main())
