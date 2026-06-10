import sys

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 找到 rv 的 innerHTML 赋值并添加保持下拉状态
old_rv = "document.getElementById('rv').innerHTML=h;"
new_rv = "document.getElementById('rv').innerHTML=h;if(FILTER_RV_SHOW){var fd=document.getElementById('filterDropdownRV');if(fd)fd.style.display='block';}"

if old_rv in content:
    content = content.replace(old_rv, new_rv)
    print("1. RV下拉状态保持已添加!")
else:
    print("1. 未找到RV innerHTML!")
    # 搜索
    idx = content.find("document.getElementById('rv').innerHTML")
    if idx >= 0:
        print(f"  在位置 {idx}: {content[idx:idx+50]}")

# 2. 验证括号平衡
def count_braces(code):
    curly = 0
    paren = 0
    i = 0
    in_str = None
    escape = False
    while i < len(code):
        c = code[i]
        if escape: escape = False; i += 1; continue
        if c == "\\": escape = True; i += 1; continue
        if in_str:
            if c == in_str: in_str = None
            i += 1; continue
        if c == "'" or c == '"': in_str = c; i += 1; continue
        if c == "{": curly += 1
        elif c == "}": curly -= 1
        elif c == "(": paren += 1
        elif c == ")": paren -= 1
        i += 1
    return curly, paren

curly, paren = count_braces(content)
print(f"2. 括号平衡: curly={curly} paren={paren}")
if curly == 0 and paren == 0:
    print("  正常!")
else:
    print(f"  不平衡: {{多{curly}个, (多{paren}个")
    # 找问题
    lines = content.split("\n")
    cum_curly = 0
    cum_paren = 0
    for i, line in enumerate(lines, 1):
        bc, bp = count_braces(line)
        cum_curly += bc
        cum_paren += bp
        if cum_curly != 0 or cum_paren != 0:
            if bc != 0 or bp != 0:
                print(f"  L{i}: +{bc}curly +{bp}paren cum={cum_curly},{cum_paren}")
            break

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("3. 保存成功!")