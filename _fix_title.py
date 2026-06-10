import sys
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    h = f.read()

# 1. Remove sd-wc-badge from title group (right after V3.3.3-Core)
old_badge = '        <span class="sd-wc-badge">2026 \u4e16\u754c\u676f\u7248</span>\n'
if old_badge in h:
    h = h.replace(old_badge, "")
    print("Removed old badge from title")
else:
    print("WARN: old badge not found")

# 2. Replace plain text status badge with capsule style
old_status = '<span style="color:rgba(255,255,255,.7);margin-left:auto;font-size:10px;white-space:nowrap"><span style="font-weight:300;color:var(--gold);font-size:9px">\u4e16\u754c\u676f</span> v3.3.3</span>'
new_status = '<span style="margin-left:auto;white-space:nowrap"><span class="sd-wc-badge">2026 \u4e16\u754c\u676f\u7248</span></span>'
if old_status in h:
    h = h.replace(old_status, new_status)
    print("Replaced status text with capsule badge")
else:
    print("WARN: old status not found")

with open(path, "w", encoding="utf-8") as f:
    f.write(h)
print("done")
