with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
with open("_snippet3.txt", "w", encoding="utf-8") as out:
    idx = html.find("function renderFromData")
    if idx >= 0:
        out.write(html[idx:idx+5000])