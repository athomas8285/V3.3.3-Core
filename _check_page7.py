import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1366, "height": 768})
        await page.goto("http://localhost:5020/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Check both the computed DOM and allDone values
        result = await page.evaluate("""
() => {
    // Check allDone in render context
    var infoList = __DATA.info || [];
    var ratingIdx = {};
    (__DATA.rating || []).forEach(function(m){ if(m.id) ratingIdx[m.id]=m; });
    var groups = {};
    for(var i = 0; i < infoList.length; i++){
        var info = infoList[i];
        var timeStr = info.time || '';
        var datePart = timeStr.length >= 10 ? timeStr.slice(0,10) : '';
        var parts = datePart.split('-');
        var dateLabel = parts.length === 3 ? parseInt(parts[1],10) + '月' + parseInt(parts[2],10) + '日' : datePart;
        if(!groups[dateLabel]) groups[dateLabel] = [];
        groups[dateLabel].push(info);
    }
    var expected = {};
    for (var dk in groups) {
        var ml = groups[dk];
        var allDone = ml.every(function(item){ var r = ratingIdx[item.id]; return r && r.actual_score; });
        expected[dk] = allDone;
    }
    
    // Check actual DOM
    var dateGroups = document.querySelectorAll('.ana-date-group');
    var actual = {};
    dateGroups.forEach(function(g) {
        var label = g.querySelector('.ana-date-label');
        var arrow = g.querySelector('.ana-date-arrow');
        var body = g.querySelector('.ana-date-body');
        if (label) {
            var text = label.textContent || '';
            var dk = '';
            var m = text.match(/(\d+月\d+日)/);
            if (m) dk = m[1];
            actual[dk] = {
                arrow: arrow ? arrow.textContent : '?',
                bodyHidden: body ? body.style.display : '?'
            };
        }
    });
    
    return JSON.stringify({expected: expected, actual: actual});
}
""")
        print("DOM check:", result)
        await browser.close()

asyncio.run(main())