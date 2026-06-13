import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1366, "height": 768})
        # Capture console
        page.on("console", lambda msg: print(f"CONSOLE: {msg.type}: {msg.text}"))
        await page.goto("http://localhost:5020/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Debug: check allDone values for each date group
        result = await page.evaluate("""
() => {
    if (typeof __DATA === 'undefined' || !__DATA.info) return 'No __DATA';
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
    var result = {};
    for (var dk in groups) {
        var ml = groups[dk];
        var allDone = ml.every(function(item){ var r = ratingIdx[item.id]; return r && r.actual_score; });
        result[dk] = {count: ml.length, allDone: allDone, ids: ml.map(function(m){return m.id;})};
    }
    return JSON.stringify(result);
}
""")
        print("Date group debug:", result)
        await browser.close()

asyncio.run(main())