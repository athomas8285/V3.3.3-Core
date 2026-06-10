from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto("http://localhost:5000/")
    
    # Wait for the page to load
    page.wait_for_selector("#historyDateList", timeout=10000)
    time.sleep(1)
    
    # Click the 2026.06.03 date item
    # The dates have data-date attribute
    item = page.query_selector('[data-date="2026-06-03"]')
    if item:
        item.click()
        time.sleep(1.5)  # wait for the API response to render
        page.screenshot(path="C:/Users/gjj/Desktop/v333/templates/screenshot.png", full_page=True)
        print("Screenshot saved")
    else:
        print("2026-06-03 item not found")
        # Debug: show all data-date items
        items = page.query_selector_all("[data-date]")
        print(f"Found {len(items)} date items")
        for it in items:
            print(f"  date={it.get_attribute('data-date')}, text={it.text_content()[:50]}")
    
    browser.close()
