import json, base64, os, re
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto("https://cbs.sports.cctv.com/worldcup2026_schedule_tabs.html", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    teams_json = page.evaluate("""() => {
        const items = document.querySelectorAll(".schedule-item");
        const found = {};
        items.forEach(item => {
            ["home","away"].forEach(side => {
                const nameEl = item.querySelector(".team."+side+" .name");
                const logoEl = item.querySelector(".team."+side+" .logo");
                if (!nameEl || !logoEl) return;
                const name = nameEl.textContent.trim();
                const style = logoEl.getAttribute("style") || "";
                const m = style.match(/url\(['"]?(data:image[^'")]+)['"]?\)/);
                if (m && !found[name]) { found[name] = m[1]; }
            });
        });
        return JSON.stringify(found);
    }""")
    teams = json.loads(teams_json)
    print(f"Extracted {len(teams)} teams")
    for n, u in sorted(teams.items()):
        print(f"  {n}")
    browser.close()
