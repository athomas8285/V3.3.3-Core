import re
f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "r", encoding="utf-8")
c = f.read()
f.close()

# Fix with raw string-based replacements
# Line 150: 历史比赛预测查?? -> 历史比赛预测查询
c = c.replace("历史比赛预测查\ufffd\ufffd", "历史比赛预测查询")

# Line 151: ↑ 倒序 button (was ??倒序)
c = c.replace('">\ufffd\ufffd\u5012\u5e8f</button>', '">\u2191 \u5012\u5e8f</button>')

# Line 155: 加载中...
c = c.replace("\u52a0\u8f7d\ufffd\ufffd", "\u52a0\u8f7d\u4e2d...")

# Line 161: 扫盘数据
c = c.replace("\ufffd\ufffd\ufffd\ufffd\u6570\u636e", "\u626b\u76d8\u6570\u636e")

# Line 163: 扫盘
c = c.replace("<em>\ufffd\ufffd\ufffd\ufffd</em>", "<em>\u626b\u76d8</em>")

# Line 273: ↓ 顺序 (sort button JS)
c = c.replace("SORT_ASC ? \"\ufffd\ufffd\u987a\u5e8f\" : \"\ufffd\ufffd\u5012\u5e8f\"", "SORT_ASC ? \"\u2193 \u987a\u5e8f\" : \"\u2191 \u5012\u5e8f\"")

# Line 300: 共' + total + '场· 命中
# Find pattern: \ufffd + total + '\ufffd\ufffd\xb7 \u547d\u4e2d
old_val = "\ufffd" + " + total + '" + "\ufffd\ufffd\xb7 " + "\u547d\u4e2d"
new_val = "' + total + '\u573a\xb7 " + "\u547d\u4e2d"  # 共' + total + '场· 命中
# Actually, let me check what the string concat actually looks like
idx = c.find("+ total +")
if idx > 0:
    ctx = repr(c[idx-5:idx+40])
    print(f"Context 'total': {ctx}")

# Line 327: 开始时间
c = c.replace("\u5f00\u59cb\u65f6\ufffd", "\u5f00\u59cb\u65f6\u95f4")

# Line 356: ht !== '—'
c = c.replace("ht !== '\ufffd\ufffd", "ht !== '\u2014'")

# Line 360: comment
c = c.replace("// Expanded \ufffd\ufffdprediction details", "// Expanded \u2014 prediction details")

# Count remaining FFFD
remaining = c.count("\ufffd")
print(f"Remaining FFFD: {remaining}")

with open("C:/Users/gjj/Desktop/v333/templates/index.html", "w", encoding="utf-8") as f:
    f.write(c)
print("DONE")
