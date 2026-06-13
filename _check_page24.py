with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
idx = html.find('var allDoneWC = ml.every')
if idx >= 0:
    ctx = html[idx:idx+350]
    with open("_verify_replacement.txt", "w", encoding="utf-8") as out:
        out.write(ctx)
    print("Replacement verified at", idx)
else:
    print("Replacement NOT found!")
    # check what's in renderFromWC
    idx2 = html.find('function renderFromWC')
    if idx2 >= 0:
        # Find the allDone or isCollapsed inside renderFromWC
        sub = html[idx2:idx2+3000]
        has_collapsed = 'isCollapsed' in sub
        has_alldone = 'allDone' in sub
        print(f"renderFromWC: has isCollapsed={has_collapsed}, has allDone={has_alldone}")