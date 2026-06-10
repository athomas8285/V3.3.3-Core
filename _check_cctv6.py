from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://cbs.sports.cctv.com/worldcup2026_schedule_tabs.html", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # Dump all IMG tags
    imgs = page.evaluate("""() => {
        return Array.from(document.querySelectorAll("img")).map(img => ({
            src: img.src,
            alt: img.alt,
            className: img.className,
            parentTag: img.parentElement ? img.parentElement.tagName : "",
            parentClass: img.parentElement ? img.parentElement.className : "",
            width: img.naturalWidth || img.width,
            height: img.naturalHeight || img.height
        }));
    }""")
    
    print(f"Total img tags: {len(imgs)}")
    for img in imgs:
        print(f"  <{img['parentTag']} class=\"{img['parentClass']}\">")
        print(f"    <img src=\"{img['src']}\" alt=\"{img['alt']}\" class=\"{img['className']}\" {img['width']}x{img['height']}>")
        print()
    
    browser.close()
