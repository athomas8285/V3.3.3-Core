with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find renderFromWC
idx = html.find('function renderFromWC')
if idx >= 0:
    # Extract the full function
    end = html.find('\nfunction ', idx + 20)
    if end < 0:
        end = len(html)
    func = html[idx:end]
    
    with open("_renderFromWC_func.txt", "w", encoding="utf-8") as out:
        out.write(func)
    
    # Check what's after the function
    after = html[end:end+100]
    with open("_after_func.txt", "w", encoding="utf-8") as out:
        out.write(after)
    
    print(f"renderFromWC function length: {len(func)}")
    print(f"Next function starts at offset: {end-idx}")