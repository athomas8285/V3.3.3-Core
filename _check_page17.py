with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
with open("_snippet12.txt", "w", encoding="utf-8") as out:
    # Find the XHR onload handler
    idx = html.find('xhr.open("GET", "/api/wc-matches"')
    if idx >= 0:
        xhr_code = html[idx:idx+2000]
        out.write(xhr_code)