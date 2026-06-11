from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1920, "height": 1080})
    page.goto("http://127.0.0.1:5000/", timeout=10000)
    page.wait_for_load_state("networkidle")
    page.screenshot(path="D:\\V3.3.3-Core\\current_page.png", full_page=True)
    b.close()
    print("OK")
