with open(r"C:\Users\gjj\Desktop\v333\templates\v4.html","r",encoding="utf-8") as f:
    c = f.read()
print("Last 200 chars:", repr(c[-200:]))
print("body tags:", c.count("<body>"), c.count("</body>"))
print("script tags:", c.count("<script>"), c.count("</script>"))
# Check for todayMatches display:none issue
dq = chr(34)
print("historyDateList ul found:", ("class="+dq+"date-list"+dq+" id="+dq+"historyDateList"+dq) in c)
print("sd-wrap found:", "sd-wrap" in c)
print("sidebar-section found:", "sidebar-section" in c)
print("date-item found:", "date-item" in c)
print("CSS date-item:", ".date-item" in c)
