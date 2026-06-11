import sys
sys.stdout.reconfigure(encoding="utf-8")
f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "r", encoding="utf-8")
lines = f.readlines()
f.close()
# Find all lines with FFFD
for i, line in enumerate(lines):
    if "\ufffd" in line:
        # Find first FFFD and show context
        for j, ch in enumerate(line):
            if ch == "\ufffd":
                start = max(0, j-8)
                end = min(len(line), j+8)
                ctx = repr(line[start:end])
                print(f"Line {i+1}: col {j}: {ctx}")
                break
