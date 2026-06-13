with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
idx = html.find("function renderFromData")
if idx >= 0:
    snippet = html[idx:idx+2500]
    with open("_verify_snippet.txt", "w", encoding="utf-8") as out:
        out.write(snippet)
    print("renderFromData length:", len(snippet))
    print("Contains 'allDone':", "allDone" in snippet)
    print("Contains 'isCollapsed':", "isCollapsed" in snippet)
    print("Contains 'actual_score':", "actual_score" in snippet)
    # Check for the line that creates date body
    date_body_idx = snippet.find("ana-date-body")
    if date_body_idx >= 0:
        near = snippet[max(0,date_body_idx-50):date_body_idx+100]
        print("Date body line:", near)