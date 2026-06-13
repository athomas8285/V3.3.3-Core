import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1366, "height": 768})
        await page.goto("http://localhost:5020/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        result = await page.evaluate("""
() => {
    var out = [];
    // Check which view is active
    var analysisInner = document.getElementById('analysisInner');
    if (!analysisInner) return 'no analysisInner';
    out.push('analysisInner exists');
    
    // Check what classes are on the parent
    var content = document.querySelector('.content');
    if (content) {
        var visibleSec = content.querySelector('.sec:not([style*=\"display:none\"]):not([style*=\"display: none\"])');
        if (visibleSec) {
            var h2 = visibleSec.querySelector('h2');
            out.push('visible section h2: ' + (h2 ? h2.textContent : 'no h2'));
        }
    }
    
    // Check date group DOM directly
    var groups = document.querySelectorAll('.ana-date-group');
    out.push('found ' + groups.length + ' date groups');
    groups.forEach(function(g, i) {
        var label = g.querySelector('.ana-date-label');
        var arrow = g.querySelector('.ana-date-arrow');
        var body = g.querySelector('.ana-date-body');
        var labelText = label ? label.textContent.trim().substring(0, 20) : 'no label';
        var arrowText = arrow ? arrow.innerHTML : 'no arrow';
        var bodyDisplay = body ? (body.style.display || '(default)') : 'no body';
        out.push('  group ' + i + ': label=' + labelText + ' arrow=' + arrowText + ' body.display=' + bodyDisplay);
    });
    
    return out.join('\\n');
}
""")
        print(result)
        await browser.close()

asyncio.run(main())