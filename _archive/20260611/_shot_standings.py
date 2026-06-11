from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:5000/", wait_until="networkidle")
    time.sleep(1)
    page.eval_on_selector("div.wc-sub-item[data-nav='standings']", "el => el.click()")
    time.sleep(0.8)
    page.screenshot(path="D:\\V3.3.3-Core\\current_standings.png", full_page=False)
    browser.close()
    print("screenshot saved")
