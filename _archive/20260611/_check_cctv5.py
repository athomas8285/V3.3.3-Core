from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://cbs.sports.cctv.com/worldcup2026_schedule_tabs.html", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # Extract all team image URLs and their nearby team names
    result = page.evaluate("""() => {
        const items = [];
        document.querySelectorAll("img").forEach(img => {
            const src = img.src || "";
            if (src.includes("sports.cctv.com/team/")) {
                const cleanSrc = src.split("?")[0];
                // Try to find the team name nearby
                let el = img.closest("[class*=team], [class*=match]") || img.parentElement;
                // Search up to 3 levels up
                for (let i = 0; i < 4; i++) {
                    if (!el) break;
                    const text = el.textContent || "";
                    // Find Chinese text that looks like a team name
                    const matches = [...text.matchAll(/[\\u4e00-\\u9fff]{2,5}/g)];
                    for (const m of matches) {
                        // Filter out non-team words
                        const name = m[0];
                        if (!["视频直播", "第1轮", "第2轮", "第3轮", "小组赛", "淘汰赛", "时间赛程", "球队赛程", "周五", "周六", "周日", "周一", "周二", "周三", "周四", "墨西哥城", "多伦多", "洛杉矶", "纽约", "波士顿", "温哥华", "休斯敦", "达拉斯", "费城", "蒙特雷", "亚特兰大", "西雅图", "迈阿密", "堪萨斯城"].includes(name)) {
                            items.push({team: name, img: cleanSrc});
                            return;
                        }
                    }
                    el = el.parentElement;
                }
            }
        });
        return items;
    }""")
    
    print(f"Found {len(result) if result else 0} team-image pairs")
    
    # Deduplicate
    seen = {}
    for r in (result or []):
        if r["team"] not in seen:
            seen[r["team"]] = r["img"]
    
    print(f"\nUnique teams: {len(seen)}")
    for t, i in seen.items():
        print(f"  {t} => {i}")
    
    # Take screenshot
    page.screenshot(path="D:\\V3.3.3-Core\\_cctv_schedule.png", full_page=True)
    print("\nScreenshot saved")
    
    browser.close()
