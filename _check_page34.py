import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1366, "height": 768})
        await page.goto("http://localhost:5020/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)
        
        result = await page.evaluate("""
() => {
    var out = [];
    // Check analysisInner
    var ai = document.getElementById('analysisInner');
    if (!ai) { out.push('no analysisInner'); return out.join('\\n'); }
    out.push('analysisInner HTML length: ' + ai.innerHTML.length);
    
    // Check date groups
    var groups = ai.querySelectorAll('.ana-date-group');
    out.push('found ' + groups.length + ' date groups');
    groups.forEach(function(g, i) {
        var label = g.querySelector('.ana-date-label');
        var arrow = g.querySelector('.ana-date-arrow');
        var body = g.querySelector('.ana-date-body');
        var labelText = label ? label.textContent.trim() : 'no label';
        var arrowText = arrow ? arrow.innerHTML : 'no arrow';
        var bodyDisplay = body ? (body.style.display || '(default)') : 'no body';
        out.push('  group ' + i + ': label=' + labelText.substring(0,15) + ' arrow=' + arrowText + ' body.display=' + bodyDisplay);
    });
    
    // Check completed cards (should have the new layout with score+half_full+hit)
    var cards = ai.querySelectorAll('.ana-card');
    var completedCards = [];
    cards.forEach(function(c) {
        var oddsGroups = c.querySelectorAll('.ana-card-odds');
        oddsGroups.forEach(function(og) {
            if (og.innerHTML.indexOf('rgba(251,191,36') >= 0) {
                completedCards.push(c);
            }
        });
    });
    out.push('found ' + completedCards.length + ' cards with gold score group');
    completedCards.forEach(function(c) {
        var num = c.querySelector('.ana-card-num');
        var oddsHtml = c.querySelector('.ana-card-odds[style*="gap:16px"]');
        out.push('  card: ' + (num ? num.textContent : '?') + ' has reflowed layout: ' + (!!oddsHtml));
        // Check for hit badge
        var allSpans = c.querySelectorAll('.ana-card-odds span');
        var hasHit = false, hasMiss = false;
        allSpans.forEach(function(s) {
            if (s.textContent === '命中') hasHit = true;
            if (s.textContent === '偏离') hasMiss = true;
        });
        out.push('    hit=' + hasHit + ' miss=' + hasMiss);
    });
    
    return out.join('\\n');
}
""")
        print(result)
        await browser.close()

asyncio.run(main())