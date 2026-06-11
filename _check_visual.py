from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1366, 'height': 768})
    page.goto('http://127.0.0.1:5020/', wait_until='networkidle')
    page.wait_for_timeout(2000)
    
    # Scroll main to bottom
    page.eval_on_selector('.main', "el => el.scrollTop = el.scrollHeight")
    page.wait_for_timeout(500)
    
    # Take viewport screenshot (shows what user sees)
    page.screenshot(path='D:/V3.3.3-Core/_screenshot_scrolled.png')
    print('Screenshot taken')
    
    # Verify disclaimer is visible in viewport
    visible = page.eval_on_selector('.ft-disclaimer', '''el => {
        const rect = el.getBoundingClientRect();
        return rect.top < window.innerHeight && rect.bottom > 0;
    }''')
    print(f'Disclaimer visible in viewport after scroll: {visible}')
    
    # Get disclaimer position relative to viewport
    pos = page.eval_on_selector('.ft-disclaimer', '''el => {
        const r = el.getBoundingClientRect();
        return {top: r.top, bottom: r.bottom, h: r.height, viewH: window.innerHeight};
    }''')
    print(f'Disclaimer viewport position: {pos}')
    
    browser.close()
