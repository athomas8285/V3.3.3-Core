from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    team_logos = []
    
    def handle_response(response):
        url = response.url
        if "cbs-img.sports.cctv.com/team/" in url and ".png" in url:
            team_logos.append(url.split("?")[0])
    
    page.on("response", handle_response)
    page.goto("https://cbs.sports.cctv.com/worldcup2026_schedule_tabs.html", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # Deduplicate
    team_logos = list(dict.fromkeys(team_logos))
    print(f"Found {len(team_logos)} unique team logos")
    
    # To map team names to logos, we need to extract the team-name:image pairs from the rendered DOM
    mapping = page.evaluate("""() => {
        // Find match cards - each has team name + flag img
        const matches = document.querySelectorAll('[class*="match"], [class*="game"], [class*="item"]');
        const results = [];
        
        // Try different selectors
        document.querySelectorAll("img").forEach(img => {
            const src = img.src || "";
            if (src.includes("cbs-img.sports.cctv.com/team/")) {
                // Find the closest parent that has a team name
                let parent = img.parentElement;
                let teamName = "";
                for (let i = 0; i < 5; i++) {
                    if (!parent) break;
                    const textNodes = parent.querySelectorAll("*");
                    for (const node of textNodes) {
                        if (node.children.length === 0 && node.textContent.trim()) {
                            const t = node.textContent.trim();
                            // Chinese team names are 2-5 chars typically
                            if (t.length >= 2 && t.length <= 7 && /[\\u4e00-\\u9fff]/.test(t)) {
                                teamName = t;
                                break;
                            }
                        }
                    }
                    if (teamName) break;
                    parent = parent.parentElement;
                }
                if (teamName) {
                    results.push({team: teamName, img: src.split("?")[0]});
                }
            }
        });
        return results;
    }""")
    
    print(f"\nTeam-to-flag mappings found: {len(mapping) if mapping else 0}")
    for m in (mapping or []):
        print(f"  {m['team']} => {m['img']}")
    
    browser.close()
