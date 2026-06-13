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
    var ai = document.getElementById('analysisInner');
    if (!ai || !ai.innerHTML.length) return 'empty';
    
    // Check completed cards
    var cards = ai.querySelectorAll('.ana-card');
    var completedCards = [];
    cards.forEach(function(c) {
        // Find gold background score groups
        var goldGroups = c.querySelectorAll('.odds-group[style*=\"rgba(251,191,36\"]');
        if (goldGroups.length > 0) {
            completedCards.push(c);
        }
    });
    out.push('completed cards with new layout: ' + completedCards.length);
    
    completedCards.forEach(function(c) {
        var num = c.querySelector('.ana-card-num');
        var topRow = c.querySelector('.ana-card-top-row');
        var id = num ? num.textContent : '?';
        out.push('  card ' + id + ':');
        
        // Check for the gap:16px container
        var gap16 = c.querySelector('.ana-card-odds[style*=\"gap:16px\"]');
        out.push('    has gap:16px container: ' + (!!gap16));
        
        if (gap16) {
            var spans = gap16.querySelectorAll('span');
            var texts = [];
            spans.forEach(function(s) { texts.push(s.textContent.trim()); });
            out.push('    content: ' + texts.join(' | '));
        }
        
        // Check for hit/miss badge
        var hitBadge = c.querySelector('.og-item[style*=\"border-radius:4px\"]');
        if (hitBadge) {
            out.push('    hit badge: ' + hitBadge.textContent + ' (color: ' + hitBadge.style.color + ')');
        }
        
        // Check for ▼
        var allText = c.textContent || '';
        out.push('    has ▼: ' + (allText.indexOf('\\u25bc') >= 0 || allText.includes('▼')));
    });
    
    return out.join('\\n');
}
""")
        print(result)
        await browser.close()

asyncio.run(main())