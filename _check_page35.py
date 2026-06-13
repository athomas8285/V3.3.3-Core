import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1366, "height": 768})
        
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        
        await page.goto("http://localhost:5020/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(5000)
        
        # Log console
        for log in console_logs:
            if 'error' in log.lower():
                print(f"CONSOLE: {log}")
        
        result = await page.evaluate("""
() => {
    var out = [];
    var ai = document.getElementById('analysisInner');
    if (!ai) { return 'no analysisInner'; }
    out.push('analysisInner HTML length: ' + ai.innerHTML.length);
    
    if (ai.innerHTML.length === 0) {
        // Check if WC_MATCHES_DATA exists
        if (typeof WC_MATCHES_DATA !== 'undefined') {
            out.push('WC_MATCHES_DATA length: ' + WC_MATCHES_DATA.length);
            // Check first few items for result
            WC_MATCHES_DATA.slice(0,5).forEach(function(m) {
                out.push('  ' + m.id + ': result=' + m.result + ' half_full=' + (m.half_full||'') + ' hit=' + m.hit);
            });
        } else {
            out.push('WC_MATCHES_DATA undefined');
        }
        return out.join('\\n');
    }
    
    var groups = ai.querySelectorAll('.ana-date-group');
    out.push('found ' + groups.length + ' date groups');
    groups.forEach(function(g, i) {
        var arrow = g.querySelector('.ana-date-arrow');
        var body = g.querySelector('.ana-date-body');
        var label = g.querySelector('.ana-date-label');
        var arrowText = arrow ? arrow.innerHTML : 'no arrow';
        var bodyDisplay = body ? (body.style.display || '(default)') : 'no body';
        var labelText = label ? label.textContent.trim().substring(0,15) : 'no label';
        out.push('  group ' + i + ': label=' + labelText + ' arrow=' + arrowText + ' body.display=' + bodyDisplay);
    });
    
    return out.join('\\n');
}
""")
        print(result)
        await browser.close()

asyncio.run(main())