with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the XHR code more precisely
idx = html.find("xhr = new XMLHttpRequest")
if idx >= 0:
    # Go back to find the IIFE start
    iife_start = html.rfind("(function", 0, idx)
    if iife_start >= 0:
        # Find the end - search for })(); after xhr.send
        send_pos = html.find("xhr.send", idx)
        if send_pos >= 0:
            # After send, find })();
            end_pos = html.find("})();", send_pos)
            if end_pos >= 0:
                end_pos += 5  # length of "})();"
                xhr_code = html[iife_start:end_pos]
                with open("_full_xhr.txt", "w", encoding="utf-8") as out:
                    out.write(xhr_code)
                print(f"XHR IIFE length: {len(xhr_code)}")
                print("Last 300 chars:")
                print(xhr_code[-300:])
            else:
                print("})(); not found after xhr.send")
        else:
            print("xhr.send not found")
    else:
        print("No (function before xhr")