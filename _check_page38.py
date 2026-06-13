with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()
idx = html.find('(function(){')
# Find the XHR IIFE
xhr_start = html.find('(function(){', html.find('xhr.open'))
if xhr_start >= 0:
    # Find the matching closing })();
    depth = 0
    end = xhr_start
    for i in range(xhr_start, min(xhr_start+5000, len(html))):
        if html[i] == '(': depth += 1
        elif html[i] == ')': depth -= 1
        if depth == 0 and html[i:i+2] == '();':
            end = i+2
            break
    xhr_code = html[xhr_start:end]
    with open("_full_xhr.txt", "w", encoding="utf-8") as out:
        out.write(xhr_code)
    print(f"XHR IIFE from {xhr_start} to {end}, length {len(xhr_code)}")
    print(xhr_code[:200])
    print("...")
    print(xhr_code[-200:])