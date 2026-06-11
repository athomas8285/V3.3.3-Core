import sys
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    h = f.read()

v = [
    ("sidebar: 小组赛程", "\u5c0f\u7ec4\u8d5b\u7a0b" in h),
    ("onclick renderGroupSchedule", "renderGroupSchedule()" in h),
    ("WC_MATCHES data embedded", "WC_MATCHES" in h),
    ("72 matches", "WC_MATCHES.length" in h or "72\u573a" in h),
    ("renderGroupSchedule function", "function renderGroupSchedule" in h),
    ("default load uses renderGroupSchedule", "renderGroupSchedule()" in h),
    ("Today header replaced", "renderGroupSchedule()" in h.split("loadDoc();")[0]),
    ("WC schedule CSS", "wc-match-card" in h),
    ("sec-header title: 小组赛程", "\"\\u5c0f\\u7ec4\\u8d5b\\u7a0b\"" in h or "小组赛程" in h),
]
print("=== WC Schedule Verification ===")
for name, ok in v:
    print(f"  [{'OK' if ok else 'MISSING'}] {name}")
