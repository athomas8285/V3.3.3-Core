import re, sys
sys.stdout.reconfigure(encoding="utf-8")
f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "r", encoding="utf-8")
c = f.read()
f.close()

# Fix replacements one by one with error handling
pairs = []

# Line 150
if "历史比赛预测查\ufffd\ufffd" in c:
    c = c.replace("历史比赛预测查\ufffd\ufffd", "历史比赛预测查询")
    print("Fixed line 150")

# Line 151
btn_old = '\ufffd\ufffd\u5012\u5e8f</button>'
if btn_old in c:
    c = c.replace(btn_old, '\u2191 \u5012\u5e8f</button>')
    print("Fixed line 151")

# Line 155
if '\u52a0\u8f7d\ufffd\ufffd' in c:
    c = c.replace('\u52a0\u8f7d\ufffd\ufffd', '\u52a0\u8f7d\u4e2d...')
    print("Fixed line 155")

# Line 161
if '\ufffd\ufffd\ufffd\ufffd\u6570\u636e' in c:
    c = c.replace('\ufffd\ufffd\ufffd\ufffd\u6570\u636e', '\u626b\u76d8\u6570\u636e')
    print("Fixed line 161")

# Line 163
if '<em>\ufffd\ufffd\ufffd\ufffd</em>' in c:
    c = c.replace('<em>\ufffd\ufffd\ufffd\ufffd</em>', '<em>\u626b\u76d8</em>')
    print("Fixed line 163")

# Line 273 - sort button JS
sort_old = 'SORT_ASC ? "\ufffd\ufffd\u987a\u5e8f" : "\ufffd\ufffd\u5012\u5e8f"'
if sort_old in c:
    c = c.replace(sort_old, 'SORT_ASC ? "\u2193 \u987a\u5e8f" : "\u2191 \u5012\u5e8f"')
    print("Fixed line 273")

# Line 300 - just find and fix
idx = c.find("+ total +")
if idx > 0:
    before = c[idx-5:idx]
    after = c[idx+9:idx+40]
    # If before contains FFFD, it's the one
    # The string looks like: ??? + total + '????· 命中' + ???
    # Check what we have
    if '\ufffd' in before:
        # Replace from prev qoute to after
        start = c.rfind("'", 0, idx)
        end = c.find("'", idx+9)
        if start >= 0 and end >= 0:
            old_str = c[start:end+1]
            new_str = "' + total + '\u573a\xb7 \u547d\u4e2d"  # 共' + total + '场· 命中
            # But we need the leading 共 too
            if start > 0 and c[start-1] == '\ufffd':
                new_full = new_str
                c = c[:start-1] + new_full + c[end+1:]
                print("Fixed line 300 (total concat)")

# Line 327
if '\u5f00\u59cb\u65f6\ufffd' in c:
    c = c.replace('\u5f00\u59cb\u65f6\ufffd', '\u5f00\u59cb\u65f6\u95f4')
    print("Fixed line 327")

# Line 356
if "ht !== '\ufffd\ufffd" in c:
    c = c.replace("ht !== '\ufffd\ufffd", "ht !== '\u2014'")
    print("Fixed line 356")

# Line 360
if "// Expanded \ufffd\ufffdprediction details" in c:
    c = c.replace("// Expanded \ufffd\ufffdprediction details", "// Expanded \u2014 prediction details")
    print("Fixed line 360")

remaining = c.count("\ufffd")
print(f"Remaining FFFD: {remaining}")
if remaining == 0:
    # Check for ? chars that should be CJK
    print("All clean!")

with open("C:/Users/gjj/Desktop/v333/templates/index.html", "w", encoding="utf-8") as f:
    f.write(c)
