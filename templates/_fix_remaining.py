f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "r", encoding="utf-8")
c = f.read()
f.close()

# Fix each known corruption by context
# 1. 历史比赛预测查?? -> 历史比赛预测查询
old1 = "\u5386\u53f2\u6bd4\u8d5b\u9884\u6d4b\u67e5" + chr(0xFFFD) + chr(0xFFFD)
new1 = "\u5386\u53f2\u6bd4\u8d5b\u9884\u6d4b\u67e5\u8be2"
c = c.replace(old1, new1)

# 2. ↑ 倒序 button
# The button text should be: ↑ 倒序
old2 = chr(0xFFFD) + chr(0xFFFD) + "\u5012\u5e8f</button>"
new2 = "\u2191 \u5012\u5e8f</button>"
c = c.replace(old2, new2)

# 3. 加载中...  
old3 = "\u52a0\u8f7d" + chr(0xFFFD) + chr(0xFFFD)
new3 = "\u52a0\u8f7d\u4e2d..."
c = c.replace(old3, new3)

# 4. 扫盘数据 / 扫盘
# In <small>????数据</small>  
old4a = "<small>" + chr(0xFFFD)*4 + "\u6570\u636e</small>"
new4a = "<small>\u626b\u76d8\u6570\u636e</small>"
c = c.replace(old4a, new4a)

# <em>????</em>
old4b = "<em>" + chr(0xFFFD)*4 + "</em>"
new4b = "<em>\u626b\u76d8</em>"
c = c.replace(old4b, new4b)

# 5. Sort button JS
old5 = "SORT_ASC ? \"" + chr(0xFFFD)*2 + "\u987a\u5e8f\" : \"" + chr(0xFFFD)*2 + "\u5012\u5e8f\""
new5 = 'SORT_ASC ? "\u2193 \u987a\u5e8f" : "\u2191 \u5012\u5e8f"'
c = c.replace(old5, new5)

# 6. String concat "共 + total + 场· 命中"
# Find pattern: ???' + total + '????· 命中' + ???
idx = c.find("+ total +")
if idx > 0:
    before_q = c.rfind("'", 0, idx)
    after_q = c.find("'", idx+9)
    if before_q >= 0 and after_q >= 0:
        old_str = c[before_q:after_q+1]
        # The old_str should be something like: '?? + total + '????· 命中' 
        # Replace with: ' + total + '\u573a· \u547d\u4e2d'  
        # But we need the leading character too
        if before_q > 0:
            # Check if there is a FFFD before the opening quote
            lead_char = c[before_q-1]
            if lead_char == chr(0xFFFD):
                # Replace 3 chars: FFFD + ' + content + '
                new_str = "' + total + '\u573a\xb7 \u547d\u4e2d"
                c = c[:before_q-1] + new_str + c[after_q+1:]
            else:
                # The text before includes the 共 character  
                # Find the start of the whole expression
                expr_start = c.rfind("'", 0, before_q-1)
                if expr_start >= 0:
                    old_expr = c[expr_start:after_q+1]
                    new_expr = "' + total + '\u573a\xb7 \u547d\u4e2d"
                    # Need to include the 共 or ? before it
                    if expr_start > 0:
                        new_expr = c[expr_start-1] + new_expr if c[expr_start-1] != "?" else new_expr
                    c = c[:expr_start] + new_expr + c[after_q+1:]

# 7. 开始时间
old7 = "\u5f00\u59cb\u65f6" + chr(0xFFFD)
new7 = "\u5f00\u59cb\u65f6\u95f4"
c = c.replace(old7, new7)

# 8. ht !== '—'
old8 = "ht !== '" + chr(0xFFFD)*2
new8 = "ht !== '\u2014"
c = c.replace(old8, new8)

# 9. Comment // Expanded — prediction details
old9 = "// Expanded " + chr(0xFFFD)*2 + "prediction details"
new9 = "// Expanded \u2014 prediction details"
c = c.replace(old9, new9)

remaining = c.count(chr(0xFFFD))
print(f"Remaining FFFD: {remaining}")

with open("C:/Users/gjj/Desktop/v333/templates/index.html", "w", encoding="utf-8") as f:
    f.write(c)
print("DONE")
