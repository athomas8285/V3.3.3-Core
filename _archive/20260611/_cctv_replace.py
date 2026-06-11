import json, base64, os, re
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto("https://cbs.sports.cctv.com/worldcup2026_schedule_tabs.html", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    teams_json = page.evaluate(r"""() => {
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
    print(f"Extracted {len(teams)} team flags from CCTV")
    # Map CCTV Chinese team names to flag keys
    name_to_key = {
        "\u58a8\u897f\u54e5":"mexico","\u5357\u975e":"south_africa","\u97e9\u56fd":"korea","\u6377\u514b":"czech",
        "\u52a0\u62ff\u5927":"canada","\u6ce2\u9ed1":"bosnia","\u7f8e\u56fd":"usa","\u5df4\u62c9\u572d":"paraguay",
        "\u5361\u5854\u5c14":"qatar","\u745e\u58eb":"switzerland","\u5df4\u897f":"brazil","\u6469\u6d1b\u54e5":"morocco",
        "\u6d77\u5730":"haiti","\u82cf\u683c\u5170":"scotland","\u6fb3\u5927\u5229\u4e9a":"australia","\u571f\u8033\u5176":"turkey",
        "\u5fb7\u56fd":"germany","\u5e93\u62c9\u7d22":"curacao","\u8377\u5170":"netherlands","\u65e5\u672c":"japan",
        "\u79d1\u7279\u8fea\u74e6":"ivory_coast","\u5384\u74dc\u591a\u5c14":"ecuador","\u745e\u5178":"sweden","\u7a81\u5c3c\u65af":"tunisia",
        "\u897f\u73ed\u7259":"spain","\u4f5b\u5f97\u89d2":"cape_verde","\u6bd4\u5229\u65f6":"belgium","\u57c3\u53ca":"egypt",
        "\u6c99\u7279\u963f\u62c9\u4f2f":"saudi","\u4e4c\u62c9\u572d":"uruguay","\u4f0a\u6717":"iran","\u65b0\u897f\u5170":"new_zealand",
        "\u6cd5\u56fd":"france","\u585e\u5185\u52a0\u5c14":"senegal","\u4f0a\u62c9\u514b":"iraq","\u632a\u5a01":"norway",
        "\u963f\u6839\u5ef7":"argentina","\u963f\u5c14\u53ca\u5229\u4e9a":"algeria","\u5965\u5730\u5229":"austria","\u7ea6\u65e6":"jordan",
        "\u8461\u8404\u7259":"portugal","\u521a\u679c\uff08\u91d1\uff09":"dr_congo","\u82f1\u683c\u5170":"england","\u514b\u7f57\u5730\u4e9a":"croatia",
        "\u52a0\u7eb3":"ghana","\u5df4\u62ff\u9a6c":"panama","\u4e4c\u5179\u522b\u514b\u65af\u5766":"uzbekistan","\u54e5\u4f26\u6bd4\u4e9a":"colombia"
    }
    flags_dir = "D:\\V3.3.3-Core\\static\\flags"
    count = 0
    for name, dataurl in teams.items():
        key = name_to_key.get(name)
        if not key:
            print(f"  WARNING: no key for {name}")
            continue
        match = re.match(r"data:image/(png|jpg|jpeg|gif);base64,(.+)", dataurl)
        if match:
            img = base64.b64decode(match.group(2))
            path = os.path.join(flags_dir, key + ".png")
            with open(path, "wb") as f:
                f.write(img)
            print(f"  {name} -> {key}.png ({len(img)} bytes)")
            count += 1
    print(f"Done - replaced {count} flag images")
    browser.close()
