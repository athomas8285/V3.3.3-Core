with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find('var isCollapsed = (dk === "6')
if idx >= 0:
    exact = html[idx:idx+350]
    with open("_exact.txt", "w", encoding="utf-8") as out:
        out.write(repr(exact))
    print(f"Found at {idx}, written to _exact.txt")