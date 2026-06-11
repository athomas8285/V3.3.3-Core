import sys
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    h = f.read()

v = [
    ("--gold CSS variable", "--gold:" in h),
    ("WC banner title", "2026 世界杯版" in h),
    ("accWCMain HTML", 'id="accWCMain"' in h),
    ("5 WC sub-items", h.count("wc-sub-item") == 5),
    ("今日赛程", "今日赛程" in h or "\\u4eca\\u65e5\\u8d5b\\u7a0b" in h),
    ("小组积分榜", "小组积分榜" in h or "\\u5c0f\\u7ec4\\u79ef\\u5206\\u699c" in h),
    ("淘汰赛对阵图", "淘汰赛对阵图" in h or "\\u6dd8\\u6c70\\u8d5b\\u5bf9\\u9635\\u56fe" in h),
    ("冠军赔率追踪", "冠军赔率追踪" in h or "\\u51a0\\u519b\\u8d54\\u7387\\u8ffd\\u8e2a" in h),
    ("今日精选推荐", "今日精选推荐" in h or "\\u4eca\\u65e5\\u7cbe\\u9009\\u63a8\\u8350" in h),
    ("accHistory preserved", 'id="accHistory"' in h),
    ("accBacktest preserved", 'id="accBacktest"' in h),
    ("accDoc preserved", 'id="accDoc"' in h),
    ("WC sub-item CSS", ".wc-sub-item{" in h),
    ("sd-wc-badge CSS", ".sd-wc-badge{" in h),
    ("No accToday in HTML", "accToday" not in h or ("accToday" not in h.split(".sd-body")[1] if ".sd-body" in h else True)),
    ("No accPlan in HTML", 'id="accPlan"' not in h),
    ("JS ref fixed", 'openAccordion("accWCMain")' in h),
    ("--glow-gold added", "--glow-gold:" in h),
    ("bg1.png path relative", "../static/bg1.png" in h),
]

print("=== Final Sidebar Verification ===")
all_ok = True
for name, ok in v:
    status = "OK" if ok else "MISSING"
    if not ok:
        all_ok = False
    print(f"  [{status}] {name}")
print(f"\n{'All checks passed!' if all_ok else 'Some checks failed - see above'}")
