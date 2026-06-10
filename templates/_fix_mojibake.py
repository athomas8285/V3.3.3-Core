f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "r", encoding="utf-8")
c = f.read()
f.close()

# Fix mojibake in non-panel sections
replacements = [
    ("\ufffd\ufffd\u5012\u5e8f", "\u2191 \u5012\u5e8f"),           # ??倒序 -> ↑ 倒序 (line 151)
    ("\u52a0\u8f7d\ufffd\ufffd", "\u52a0\u8f7d\u4e2d..."),         # 加载?? -> 加载中... (line 155)
    ("\ufffd\ufffd\ufffd\ufffd\u6570\u636e", "\u626b\u76d8\u6570\u636e"),  # ????数据 -> 扫盘数据 (line 161)
    ("<em>\ufffd\ufffd\ufffd\ufffd</em>", "<em>\u626b\u76d8</em>"),  # <em>????</em> -> <em>扫盘</em> (line 163)
    ("\ufffd\ufffd\u987a\u5e8f", "\u2193 \u987a\u5e8f"),           # ??顺序 -> ↓ 顺序 (line 273)
    ("\u5f00\u59cb\u65f6\ufffd", "\u5f00\u59cb\u65f6\u95f4"),       # 开始时?? -> 开始时间 (line 327)
    ("// Expanded \ufffd\ufffdprediction details", "// Expanded \u2014 prediction details"),  # (line 360)
    ("ht !== '\ufffd\ufffd", "ht !== '\u2014'"),                    # ht !== '?? -> ht !== '—' (line 356)
]

for old, new in replacements:
    if old in c:
        c = c.replace(old, new)
        print(f"Fixed: {repr(old[:30])} -> {repr(new[:30])}")
    else:
        print(f"Not found: {repr(old[:30])}")

# Fix specific string concat pattern (line 300)
# Original: 共? + total + '场· 命中' 
# But the code uses unicode escapes, so we need to find the actual bytes
# The line contains: '\ufffd + total + \'\ufffd\ufffd\xb7 \u547d\u4e2d'
target = "\ufffd" + " + total + '" + "\ufffd\ufffd\xb7 "
replacement = "' + total + '\u573a\xb7 "  # 场·
# Actually let me just check the raw bytes
import re
# Find the pattern more carefully
idx = c.find("total + '")
if idx > 0:
    ctx = c[idx-10:idx+30]
    print(f"Context around 'total': {repr(ctx)}")

# Count remaining FFFD
remaining = c.count("\ufffd")
print(f"Remaining FFFD: {remaining}")

with open("C:/Users/gjj/Desktop/v333/templates/index.html", "w", encoding="utf-8") as f:
    f.write(c)
print("DONE")
