from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":900})
    pg.goto("http://localhost:5020/",wait_until="networkidle")
    pg.evaluate("switchNav('analysis')")
    time.sleep(3)
    pg.screenshot(path="D:\\V3.3.3-Core\\data\\analysis_screenshot.png",full_page=True)
    b.close()
    print("Screenshot OK")
