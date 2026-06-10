import sys
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    h = f.read()
v = [
    ("SVG home icon", "sd-home" in h),
    ("Tooltip title", "\u8fd4\u56de\u9996\u9875" in h),
    ("today-item CSS", "today-item .d" in h),
    ("hist-item CSS", "hist-item .d" in h),
    ("today-item in JS", "today-item" in h),
    ("hist-item in JS", "hist-item" in h),
    ("today click handler", 'd==="today"' in h),
    ("Deduplication", "seen[d]" in h),
    ("Sort descending", "da > db ? -1" in h),
    ("Filter today", "HISTORY_TODAY_STR" in h),
]
print("Sidebar verification after restore + fixes:")
for name, ok in v:
    print(f"  [{'OK' if ok else 'MISSING'}] {name}")
