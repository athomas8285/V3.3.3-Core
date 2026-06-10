import time
from playwright.sync_api import sync_playwright

url = "http://127.0.0.1:5000/"
output = r"D:\V3.3.3-Core\templates\standings_check.png"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(url, wait_until="networkidle")
    time.sleep(1)
    
    # Click the standings nav
    # Try various selectors
    try:
        # Try clicking the sub-item for standings
        standings_btn = page.query_selector('[data-nav="standings"]')
        if standings_btn:
            standings_btn.click()
            time.sleep(1)
            print("Clicked standings via data-nav")
        else:
            print("No data-nav=standings found")
            # List all sub-items
            items = page.query_selector_all('.wc-sub-item')
            for item in items:
                txt = item.inner_text()
                nav = item.get_attribute('data-nav')
                print(f"  sub-item: {txt} nav={nav}")
    except Exception as e:
        print(f"Click error: {e}")
    
    time.sleep(1)
    page.screenshot(path=output, full_page=False)
    browser.close()
    print(f"Screenshot saved to {output}")