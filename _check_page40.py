with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find("xhr = new XMLHttpRequest")
iife_start = html.rfind("(function", 0, idx)
send_pos = html.find("xhr.send", idx)
if send_pos >= 0:
    end_pos = html.find("})();", send_pos)
    if end_pos >= 0:
        end_pos += 5
        xhr_code = html[iife_start:end_pos]
        with open("_full_xhr_current.txt", "w", encoding="utf-8") as out:
            out.write(xhr_code)
        print(f"Length: {len(xhr_code)}")
        print("\n=== FULL XHR CODE ===")
        print(xhr_code)