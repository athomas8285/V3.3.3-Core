import sys

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

rr_start = None
rr_end = None
for i, line in enumerate(lines):
    if "function renderReview()" in line:
        rr_start = i
    if rr_start and "window.onload" in line:
        rr_end = i
        break

if rr_start and rr_end:
    print(f"renderReview 行 {rr_start+1} - {rr_end}")
    for i in range(rr_start, rr_end):
        line = lines[i]
        if "yr.forEach" in line or ".forEach" in line or "if(yr.length)" in line:
            print(f"  L{i+1}: {line[:150].rstrip()}")