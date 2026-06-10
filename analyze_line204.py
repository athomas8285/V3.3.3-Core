import sys

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 仔细分析L204 - 提取非字符串部分
line = lines[203]  # 0-indexed
print(f"L204长度: {len(line)} 字符")

# 找出真正在代码中的括号（不在字符串内的）
curly_opens = []
curly_closes = []
paren_opens = []
paren_closes = []

i = 0
in_str = None
escape = False
pos_in_code = []

while i < len(line):
    c = line[i]
    
    if escape:
        escape = False
        i += 1
        continue
    
    if c == "\\":
        escape = True
        i += 1
        continue
    
    if in_str:
        if c == in_str:
            in_str = None
        i += 1
        continue
    
    if c == "'" or c == '"':
        in_str = c
        i += 1
        continue
    
    if c == "{":
        curly_opens.append(i)
        pos_in_code.append((i, "{"))
    elif c == "}":
        curly_closes.append(i)
        pos_in_code.append((i, "}"))
    elif c == "(":
        paren_opens.append(i)
        pos_in_code.append((i, "("))
    elif c == ")":
        paren_closes.append(i)
        pos_in_code.append((i, ")"))
    
    i += 1

print(f"\n代码括号统计:")
print(f"  {{ {len(curly_opens)}个, }} {len(curly_closes)}个")
print(f"  ( {len(paren_opens)}个, ) {len(paren_closes)}个")
print(f"  净额: {len(curly_opens)-len(curly_closes)}个{{, {len(paren_opens)-len(paren_closes)}个(")

# 找出未匹配的
print(f"\n所有代码括号位置及上下文:")
for pos, char in pos_in_code:
    ctx = line[max(0,pos-15):pos+15].replace("\n", "\\n")
    print(f"  位置{pos}: {char} -> ...{ctx}...")