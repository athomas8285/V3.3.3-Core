with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
with open("_snippet7.txt", "w", encoding="utf-8") as out:
    # Find tab switching code
    idx = html.find("case 'analysisContent'")
    if idx >= 0:
        ctx = html[max(0,idx-200):idx+300]
        out.write("=== Tab switch context ===\n")
        out.write(ctx)
        out.write("\n\n")
    
    # Find onload or DOMContentLoaded
    for evt in ["onload", "DOMContentLoaded", "addEventListener"]:
        idx = html.find(evt)
        if idx >= 0:
            ctx = html[max(0,idx-50):idx+200]
            out.write(f"=== {evt} at {idx} ===\n")
            out.write(ctx)
            out.write("\n\n")