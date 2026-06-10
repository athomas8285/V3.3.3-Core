import sys
import re
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    h = f.read()

# 1. Find and extract WC_MATCHES data + renderGroupSchedule from inside else block
#   Start marker: "// 2026 \u4e16\u754c\u676f \u5c0f\u7ec4\u8d5b 72\u573a\u5bf9\u9635"
#   End marker: "return false;\n}\n\nif(typeof __DATA"

start_marker = "// 2026 \u4e16\u754c\u676f \u5c0f\u7ec4\u8d5b 72\u573a\u5bf9\u9635\nvar WC_MATCHES"
end_marker = "return false;\n}\n\nif(typeof __DATA"

s = h.find(start_marker)
e = h.find(end_marker, s)
if s >= 0 and e > s:
    # Extract the block
    block = h[s:e]  # This goes from the comment to "return false;\n}"
    # Remove it from current position
    h = h[:s] + h[e:]
    # Insert at top level - right after the <script> tag + first variables
    insert_point = h.find("function toggleAccordion")
    if insert_point >= 0:
        h = h[:insert_point] + block + "\n\n" + h[insert_point:]
        print(f"Moved block ({len(block)} chars) to top level")
    else:
        print("ERROR: insert point not found")
else:
    print(f"ERROR: markers not found (s={s}, e={e})")

with open(path, "w", encoding="utf-8") as f:
    f.write(h)
print("done")
