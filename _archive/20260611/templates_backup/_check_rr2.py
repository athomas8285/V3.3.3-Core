with open("charts.js","r",encoding="utf-8") as f:
    t = f.read()
idx = t.index("function renderReview()")
# Find the end - look for the next function or end of file
rest = t[idx:]
# Find the full function body by counting braces
depth = 0
started = False
for i,ch in enumerate(rest):
    if ch == "{":
        depth += 1
        started = True
    elif ch == "}":
        depth -= 1
        if started and depth == 0:
            print(rest[:i+1])
            break