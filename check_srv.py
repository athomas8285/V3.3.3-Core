import urllib.request
resp = urllib.request.urlopen("http://localhost:8080/v4.html")
html = resp.read().decode("utf-8-sig")
print("File size:", len(html))
dq = chr(34)
print("Has date-list:", ("class="+dq+"date-list"+dq) in html)
print("Has historyDateList:", ("id="+dq+"historyDateList"+dq) in html)
print("Has date-item:", "date-item" in html)
idx = html.find("function renderDateList")
print("renderDateList found:", idx >= 0)
if idx >= 0:
    end = html.find("\n}\n", idx)
    print(html[idx:end+4])
