with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
with open("_snippet9.txt", "w", encoding="utf-8") as out:
    # Find the analysisContent section in the HTML
    idx = html.find('id="analysisContent"')
    if idx >= 0:
        ctx = html[idx:idx+500]
        out.write("=== analysisContent ===\n")
        out.write(ctx)
        out.write("\n\n")
    
    # Find analysisInner
    idx = html.find('id="analysisInner"')
    if idx >= 0:
        ctx = html[max(0,idx-100):idx+500]
        out.write("=== analysisInner ===\n")
        out.write(ctx)