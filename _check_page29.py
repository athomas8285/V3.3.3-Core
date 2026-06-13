with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
# Find the XHR handler and WC_MATCHES_DATA construction
idx = html.find("xhr.open")
if idx >= 0:
    xhr_code = html[idx:idx+1200]
    with open("_xhr_handler.txt", "w", encoding="utf-8") as out:
        out.write(xhr_code)
    print("XHR handler found")