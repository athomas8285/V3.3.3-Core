import sys
sys.stdout.reconfigure(encoding="utf-8")
f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "r", encoding="utf-8")
lines = f.readlines()
f.close()
bad_indices = [149,150,154,160,162,272,299,326,355,359]  # 0-indexed
for i in bad_indices:
    if i < len(lines):
        line = lines[i]
        # Show hex of the FFFD area
        for j, ch in enumerate(line):
            if ch == "\ufffd":
                ctx = line[max(0,j-10):j+10]
                print(f"Line {i+1} pos {j}: ...{repr(ctx)}...")
                break
