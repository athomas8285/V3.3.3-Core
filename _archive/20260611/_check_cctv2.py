from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://cbs.sports.cctv.com/worldcup2026_schedule_tabs.html", wait_until="networkidle", timeout=30000)
    
    # Wait for content to load
    page.wait_for_timeout(3000)
    
    # Get all images
    result = page.evaluate("""() => {
        const imgs = document.querySelectorAll('img');
        return Array.from(imgs)
            .filter(img => img.src && (img.src.includes('.png') || img.src.includes('.svg') || img.src.includes('.jpg')))
            .map(img => ({
                src: img.src,
                w: img.naturalWidth || img.width,
                h: img.naturalHeight || img.height,
                alt: img.alt || img.title || ""
            }));
    }""")
    
    print(f"Total images found: {len(result) if result else 0}")
    print("="*70)
    for r in (result or []):
        print(f"  {r['w']}x{r['h']} | {r['src']}")
    
    # Take screenshot
    page.screenshot(path="D:\\V3.3.3-Core\\_cctv_screenshot.png", full_page=True)
    print("\nScreenshot saved")
    
    browser.close()
