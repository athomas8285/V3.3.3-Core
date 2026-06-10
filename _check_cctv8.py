from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://cbs.sports.cctv.com/worldcup2026_schedule_tabs.html", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # Capture ALL background images and element styles with team logos
    result = page.evaluate("""() => {
        const items = [];
        const allEls = document.querySelectorAll("*");
        allEls.forEach(el => {
            const style = window.getComputedStyle(el);
            const bg = style.backgroundImage || "";
            if (bg && bg.includes("sports.cctv.com/team/")) {
                items.push({
                    tag: el.tagName,
                    bg: bg,
                    text: (el.textContent || "").trim().substring(0, 30)
                });
            }
        });
        return items;
    }""")
    
    print(f"Elements with team logo backgrounds: {len(result) if result else 0}")
    for r in (result or []):
        print(f"  <{r['tag']}> bg={r['bg'][:80]}... text=\"{r['text']}\"")
    
    # Also dump the rendered page HTML for team-related sections
    html = page.content()
    # Look for any data attributes with team info
    import re
    # Find style tags with team URLs
    style_urls = re.findall(r"cbs-img\.sports\.cctv\.com/team/[^\s\"'()]+", html)
    print(f"\nTeam URLs in HTML: {len(style_urls)}")
    for u in list(dict.fromkeys(style_urls)):
        print(f"  {u}")
    
    browser.close()
