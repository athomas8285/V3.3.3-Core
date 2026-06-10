from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    api_calls = []
    def handle_request(req):
        url = req.url
        if ".json" in url or "api" in url or "worldcup" in url or "schedule" in url or "match" in url or "team" in url:
            api_calls.append(url)
    
    page.on("request", handle_request)
    page.goto("https://cbs.sports.cctv.com/worldcup2026_schedule_tabs.html", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(5000)
    
    print("=== API Calls ===")
    for u in api_calls:
        print(f"  {u}")
    
    # Check page text content for team names
    text = page.evaluate("() => document.body.innerText")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    print(f"\n=== Page text (first 50 lines) ===")
    for l in lines[:50]:
        print(f"  {l}")
    
    # Check for canvas or SVG elements
    svg_imgs = page.evaluate("""() => {
        const svgs = document.querySelectorAll('svg');
        const canvases = document.querySelectorAll('canvas');
        return {
            svgCount: svgs.length,
            canvasCount: canvases.length
        };
    }""")
    print(f"\nSVGs: {svg_imgs['svgCount']}, Canvases: {svg_imgs['canvasCount']}")
    
    browser.close()
