from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    team_data = {}  # team_name -> flag_url
    
    def handle_request(req):
        url = req.url
        if "cbs-img.sports.cctv.com/team/" in url:
            # The URL will be requested with some context we can capture
            pass
    
    def handle_response(resp):
        url = resp.url
        if "cbs-img.sports.cctv.com/team/" in url:
            # Get the element that triggered this request
            pass
    
    page.on("response", lambda resp: handle_response(resp))
    page.goto("https://cbs.sports.cctv.com/worldcup2026_schedule_tabs.html", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # Dump the full HTML
    html = page.content()
    # Save it
    with open("D:\\V3.3.3-Core\\_cctv_rendered.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"HTML size: {len(html)} bytes")
    
    # Search for team logo URLs in the HTML
    import re
    urls = re.findall(r"https://cbs-img\.sports\.cctv\.com/team/[^\'\"]+", html)
    deduped = list(dict.fromkeys(urls))
    print(f"\nFound {len(deduped)} unique team logo URLs in HTML")
    for u in deduped:
        print(f"  {u}")
    
    # Also search for team names near these URLs in the HTML
    for u in deduped[:2]:
        # Find context around this URL
        idx = html.find(u)
        if idx > 0:
            context = html[max(0,idx-200):idx+len(u)+200]
            print(f"\nContext for {u}:")
            print(context)
            print()
    
    browser.close()
