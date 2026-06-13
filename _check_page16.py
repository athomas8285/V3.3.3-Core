import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1366, "height": 768})
        
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"{msg.type}: {msg.text}"))
        
        await page.goto("http://localhost:5020/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Check what's in analysisInner
        ai_html = await page.evaluate("document.getElementById('analysisInner').innerHTML.length")
        print(f"analysisInner HTML length: {ai_html}")
        print(f"analysisInner is empty: {ai_html == 0}")
        
        # Check which view is visible
        visible = await page.evaluate("""
() => {
    var views = document.querySelectorAll('.view-content');
    var result = [];
    views.forEach(function(v) {
        if (v.style.display !== 'none') {
            result.push(v.id || v.className);
        }
    });
    return result.join(', ');
}
""")
        print(f"Visible views: {visible}")
        
        # Check homeInner
        hi_html = await page.evaluate("document.getElementById('homeInner') ? document.getElementById('homeInner').innerHTML.length : -1")
        print(f"homeInner HTML length: {hi_html}")
        
        # Check if there's a WC_MATCHES_DATA XHR response
        for log in console_logs:
            if 'error' in log.lower() or 'warn' in log.lower():
                print(f"CONSOLE: {log}")
        
        await browser.close()

asyncio.run(main())