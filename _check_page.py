with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
with open("_snippet2.txt", "w", encoding="utf-8") as out:
    # Find renderFromWC
    idx = html.find("function renderFromWC")
    if idx >= 0:
        out.write("=== renderFromWC ===\n")
        out.write(html[idx:idx+3000])
    # Check if renderFromWC has date grouping with allDone
    idx2 = html.find("renderFromWC", idx+100) if idx >= 0 else -1
    if idx2 >= 0:
        pass
    # Find all render functions
    for fn in ["renderFromData", "renderFromWC"]:
        pos = html.find("function " + fn)
        if pos >= 0:
            out.write(f"\n=== {fn} at {pos} ===\n")