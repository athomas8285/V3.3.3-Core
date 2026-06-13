with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
# Check how many times isCollapsed appears
count = html.count('isCollapsed')
print(f"'isCollapsed' appears {count} times")

# Also check what the allDoneWC replacement looks like
idx = html.find('allDoneWC')
if idx >= 0:
    ctx = html[idx:idx+350]
    with open("_final_replacement.txt", "w", encoding="utf-8") as out:
        out.write(ctx)
    print("allDoneWC found at", idx)