import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1366, "height": 768})
        await page.goto("http://localhost:5020/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        
        # Inject logging and re-run renderFromData to capture the exact output
        result = await page.evaluate("""
() => {
    // Clone renderFromData to capture output
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
    var dateKeys = Object.keys(groups).sort(function(a,b){
        function toNum(s){ var m=s.match(/(\d+)月(\d+)日/); return m?parseInt(m[1],10)*100+parseInt(m[2],10):0; }
        return toNum(a)-toNum(b);
    });
    
    var debug = [];
    for(var di = 0; di < dateKeys.length; di++){
        var dk = dateKeys[di];
        var ml = groups[dk];
        debug.push('=== ' + dk + ' ===');
        for(var mi = 0; mi < ml.length; mi++){
            var item = ml[mi];
            var r = ratingIdx[item.id];
            debug.push('  item.id=' + item.id + ' ratingIdx exists=' + (!!r) + ' actual_score=' + (r ? r.actual_score : 'N/A'));
        }
        var allDone = ml.every(function(item){ var r = ratingIdx[item.id]; return r && r.actual_score; });
        debug.push('  allDone=' + allDone);
    }
    return debug.join('\\n');
}
""")
        print("Debug:", result)
        await browser.close()

asyncio.run(main())