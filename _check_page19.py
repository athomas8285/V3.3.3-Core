with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_text = '''    var isCollapsed = (dk === "6\\u670812\\u65e5");
    h += '<div class="ana-date-group">';
    h += '<div class="ana-date-label clickable" onclick="toggleDateGroup(this)">';
    h += '<span class="ana-date-arrow">' + (isCollapsed ? '\\u25b6' : '\\u25bc') + '</span> 📅 ' + dk + '<span class="adl-count">' + ml.length + ' 场</span></div>';
    h += '<div class="ana-date-body"' + (isCollapsed ? ' style="display:none"' : '') + '>';'''

new_text = '''    var allDoneWC = ml.every(function(m){ return !!m.result; });
    h += '<div class="ana-date-group">';
    h += '<div class="ana-date-label clickable" onclick="toggleDateGroup(this)">';
    h += '<span class="ana-date-arrow">' + (allDoneWC ? '\\u25b6' : '\\u25bc') + '</span> 📅 ' + dk + '<span class="adl-count">' + ml.length + ' 场</span></div>';
    h += '<div class="ana-date-body"' + (allDoneWC ? ' style="display:none"' : '') + '>';'''

count = html.count(old_text)
print(f"Found: {count}")

if count > 0:
    html = html.replace(old_text, new_text)
    with open("D:\\V3.3.3-Core\\templates\\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Replaced!")
else:
    # Try reading the exact bytes
    idx = html.find('var isCollapsed = (dk === "6')
    if idx >= 0:
        exact = html[idx:idx+350]
        print("Exact text (repr):")
        print(repr(exact))