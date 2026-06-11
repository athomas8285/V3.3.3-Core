import sys

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 逐行检查代码括号（排除字符串内的）
def line_balance(line):
    curly = 0
    paren = 0
    i = 0
    in_str = None
    escape = False
    regex = False
    
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
            curly += 1
        elif c == "}":
            curly -= 1
        elif c == "(":
            paren += 1
        elif c == ")":
            paren -= 1
        
        i += 1
    
    return curly, paren

cum_curly = 0
cum_paren = 0
for i, line in enumerate(lines, 1):
    bc, bp = line_balance(line)
    cum_curly += bc
    cum_paren += bp
    if cum_curly != 0 or cum_paren != 0:
        if bc != 0 or bp != 0:
            print(f"L{i:4d}: +{bc}curly +{bp}paren | cum={cum_curly},{cum_paren} | {line[:120].rstrip()}")