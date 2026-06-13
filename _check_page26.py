with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the renderFromWC card rendering for completed matches
idx = html.find('function renderFromWC')
if idx >= 0:
    sub = html[idx:idx+5000]
    with open("_renderFromWC_full.txt", "w", encoding="utf-8") as out:
        out.write(sub)
    print("renderFromWC written, length", len(sub))