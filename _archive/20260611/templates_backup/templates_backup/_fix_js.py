# Read the file and fix the renderDateList JS line
f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "rb")
c = f.read()
f.close()

# Find the corrupted line in binary
# The line we need to find has: </div>>' + total + '场· 命中场· 命中' + hits + '
pattern = b"</div>>' + total + "
idx = c.find(pattern)
if idx >= 0:
    # Find the start and end of this line
    line_start = c.rfind(b"\n", 0, idx) + 1
    line_end = c.find(b"\n", idx)
    print(f"Corrupted line: {c[line_start:line_end]}")
    print()
    
    # Find the next line too
    next_line_end = c.find(b"\n", line_end + 1)
    print(f"Next line: {c[line_end+1:next_line_end]}")
else:
    print("Pattern not found, trying alternatives")
    # Search for what actually exists
    idx2 = c.find(b"+ total +")
    if idx2 >= 0:
        line_start2 = c.rfind(b"\n", 0, idx2) + 1
        line_end2 = c.find(b"\n", idx2)
        print(f"Found + total + at {idx2}: {c[line_start2:line_end2]}")
