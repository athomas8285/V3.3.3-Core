import subprocess
import tempfile
import os

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"

# Check for JS syntax using node if available
try:
    result = subprocess.run(["node", "--check", path], capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print("Node.js syntax check: PASS")
    else:
        print("Node.js syntax error:")
        print(result.stderr)
except FileNotFoundError:
    print("Node.js not available, using Python-based check")

# Python-based check: see if the h variable assignment has issues
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Check if the problematic line starts with "var h=" and has proper structure
idx = content.find("var h='<div class=\"sec\"")
if idx >= 0:
    # Find the end of the var h statement
    end = content.find(";", idx)
    stmt = content[idx:end+1]
    
    # Count actual code braces (not in strings)
    in_string = False
    in_single = False
    escape = False
    code_braces = 0
    code_parens = 0
    
    for c in stmt:
        if escape:
            escape = False
            continue
        if c == "\\":
            escape = True
            continue
        if c == "'" and not in_string:
            in_single = not in_single
            continue
        if c == '"' and in_single:
            continue  # quotes inside single-quoted strings
        if not in_single:
            if c == "{":
                code_braces += 1
            elif c == "}":
                code_braces -= 1
            elif c == "(":
                code_parens += 1
            elif c == ")":
                code_parens -= 1
    
    print(f"var h line: code braces={code_braces}, code parens={code_parens}")