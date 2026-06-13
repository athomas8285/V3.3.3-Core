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
        await page.wait_for_timeout(3000)
        
        for log in all_console:
            if 'error' in log.lower():
                print(f"CONSOLE: {log}")
        
        result = await page.evaluate("""
() => {
    var out = [];
    var ai = document.getElementById('analysisInner');
    if (!ai) return 'no analysisInner';
    out.push('analysisInner HTML length: ' + ai.innerHTML.length);
    
    if (ai.innerHTML.length === 0) {
        out.push('WC_MATCHES_DATA: ' + (typeof WC_MATCHES_DATA !== 'undefined' ? WC_MATCHES_DATA.length : 'UNDEFINED'));
        return out.join('\\n');
    }
    
    var groups = ai.querySelectorAll('.ana-date-group');
    out.push('found ' + groups.length + ' date groups');
    groups.forEach(function(g, i) {
        var arrow = g.querySelector('.ana-date-arrow');
        var body = g.querySelector('.ana-date-body');
        var arrowText = arrow ? arrow.innerHTML : 'no arrow';
        var bodyDisplay = body ? (body.style.display || '(default)') : 'no body';
        out.push('  group ' + i + ': arrow=' + arrowText + ' body.display=' + bodyDisplay);
    });
    
    return out.join('\\n');
}
""")
        print(result)
        await browser.close()

asyncio.run(main())