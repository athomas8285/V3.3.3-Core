with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find all XHR related code
for pat in ['xhr.open', 'XMLHttpRequest', '/api/wc-matches']:
    idx = html.find(pat)
    if idx >= 0:
        ctx = html[max(0,idx-50):idx+100]
        with open("_xhr_check.txt", "w", encoding="utf-8") as out:
            out.write(pat + " found at " + str(idx) + "\n" + ctx)
        print(f"'{pat}' found at {idx}: {ctx[:100]}")
    else:
        print(f"'{pat}' NOT found")