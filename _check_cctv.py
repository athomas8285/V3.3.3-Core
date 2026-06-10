from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Flag image collector
    flags_found = []
    
    def handle_response(response):
        url = response.url
        if ".png" in url and "team" in url.lower() or "flag" in url.lower():
            try:
                body = response.text()
                flags_found.append({"url": url})
            except:
                pass
    
    page.on("response", handle_response)
    page.goto("https://worldcup.cctv.com/2026/schedule/index.shtml", wait_until="networkidle", timeout=30000)
    
    # Find all team flag images in the iframe
    result = page.evaluate("""() => {
        const imgs = document.querySelectorAll('img');
        return Array.from(imgs)
            .filter(img => img.src && (img.src.includes('.png') || img.src.includes('flag')))
            .map(img => ({
                src: img.src,
                width: img.naturalWidth || img.width,
                height: img.naturalHeight || img.height,
                alt: img.alt || ''
            }));
    }""")
    print("=== Images found on main page ===")
    for r in (result or []):
        print(f"  {r}")

    # Try iframe content
    iframe_result = page.evaluate("""() => {
        const iframe = document.getElementById('iframe');
        if (!iframe) return null;
        try {
            const doc = iframe.contentDocument || iframe.contentWindow.document;
            const imgs = doc.querySelectorAll('img');
            return Array.from(imgs)
                .filter(img => img.src && (img.src.includes('.png') || img.src.includes('svg')))
                .map(img => ({
                    src: img.src,
                    width: img.naturalWidth || img.width,
                    height: img.naturalHeight || img.height,
                    alt: img.alt || ''
                }));
        } catch(e) {
            return 'iframe access denied: ' + e.message;
        }
    }""")
    print()
    print("=== Iframe images ===")
    if iframe_result:
        if isinstance(iframe_result, str):
            print(f"  {iframe_result}")
        else:
            for r in iframe_result:
                print(f"  {r}")
    
    # Also try to get the iframe src
    iframe_src = page.evaluate("() => document.getElementById('iframe')?.src")
    print(f"\nIframe src: {iframe_src}")
    
    browser.close()
