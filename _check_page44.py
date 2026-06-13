import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1366, "height": 768})
        await page.goto("http://localhost:5020/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Navigate to analysis tab to see renderFromData
        await page.evaluate("switchNav('analysis')")
        await page.wait_for_timeout(1000)
        
        await page.screenshot(path="D:\\V3.3.3-Core\\verify_now.png", full_page=True)
        
        # Verify renderFromData also has correct layout
        result = await page.evaluate("""
() => {
    var out = [];
    var ai = document.getElementById('analysisInner');
    if (!ai) return 'no analysisInner';
    
    var groups = ai.querySelectorAll('.ana-date-group');
    groups.forEach(function(g) {
        var arrow = g.querySelector('.ana-date-arrow');
        var body = g.querySelector('.ana-date-body');
        var label = g.querySelector('.ana-date-label');
        var arrowText = arrow ? arrow.innerHTML : '?';
        var bodyDisplay = body ? (body.style.display || '(default)') : '?';
        var dk = label ? label.textContent.trim().substring(0,8) : '?';
        out.push(dk + ': arrow=' + arrowText + ' body=' + bodyDisplay);
    });
    
    // Check completed cards
    var cards = ai.querySelectorAll('.ana-card');
    var compCards = [];
    cards.forEach(function(c) {
        var gold = c.querySelector('.odds-group[style*=\"rgba(251,191,36\"]');
        if (gold) compCards.push(c);
    });
    out.push('completed cards: ' + compCards.length);
    compCards.forEach(function(c) {
        var num = c.querySelector('.ana-card-num');
        out.push('  ' + (num ? num.textContent : '?') + ': has gold score group');
    });
    
    return out.join('\\n');
}
""")
        print(result)
        await browser.close()

asyncio.run(main())