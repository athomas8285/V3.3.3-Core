with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find('var isCollapsed = (dk === "6')
# Read exact text
exact = html[idx:idx+350]
with open("_exact2.txt", "w", encoding="utf-8") as out:
    for i, c in enumerate(exact):
        out.write(f"{i}: U+{ord(c):04X} {repr(c)}")
        if c == '\n':
            out.write("\\n")
        out.write("\n")
print("Done")