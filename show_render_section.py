import sys

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# L306附近 - 渲染循环
for i in range(304, 312):
    print(f"L{i+1}: {lines[i][:200].rstrip()}")
print()
# L305 - if(yr.length) 之前
for i in range(275, 295):
    print(f"L{i+1}: {lines[i][:200].rstrip()}")