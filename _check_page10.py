with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
with open("_snippet6.txt", "w", encoding="utf-8") as out:
    # search for renderAnalysisView calls
    idx = 0
    while True:
        idx = html.find("renderAnalysisView", idx)
        if idx < 0: break
        ctx = html[max(0,idx-50):idx+80]
        out.write(f"At {idx}: ...{ctx}...\n")
        idx += 1
    
    out.write("\n\n=== renderFromWC near ===\n")
    idx = html.find("function renderFromWC")
    if idx >= 0:
        out.write(html[idx:idx+2000])