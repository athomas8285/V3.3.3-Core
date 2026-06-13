with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_text = '''    var isCollapsed = (dk === "6\u670812\u65e5");
    h += '<div class="ana-date-group">';
    h += '<div class="ana-date-label clickable" onclick="toggleDateGroup(this)">';
    h += '<span class="ana-date-arrow">' + (isCollapsed ? '\\u25b6' : '\\u25bc') + '</span> 📅 ' + dk + '<span class="adl-count">' + ml.length + ' 场</span></div>';
    h += '<div class="ana-date-body"' + (isCollapsed ? ' style="display:none"' : '') + '>';'''

# The file has actual chars not escape sequences
old_text_actual = '''    var isCollapsed = (dk === "6月12日");
    h += '<div class="ana-date-group">';
    h += '<div class="ana-date-label clickable" onclick="toggleDateGroup(this)">';
    h += '<span class="ana-date-arrow">' + (isCollapsed ? '▶' : '▼') + '</span> 📅 ' + dk + '<span class="adl-count">' + ml.length + ' 场</span></div>';
    h += '<div class="ana-date-body"' + (isCollapsed ? ' style="display:none"' : '') + '>';'''

new_text_actual = '''    var allDoneWC = ml.every(function(m){ return !!m.result; });
    h += '<div class="ana-date-group">';
    h += '<div class="ana-date-label clickable" onclick="toggleDateGroup(this)">';
    h += '<span class="ana-date-arrow">' + (allDoneWC ? '▶' : '▼') + '</span> 📅 ' + dk + '<span class="adl-count">' + ml.length + ' 场</span></div>';
    h += '<div class="ana-date-body"' + (allDoneWC ? ' style="display:none"' : '') + '>';'''

count = html.count(old_text_actual)
print(f"Found: {count}")

if count > 0:
    html = html.replace(old_text_actual, new_text_actual)
    with open("D:\\V3.3.3-Core\\templates\\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Replaced!")
else:
    print("Still not found, checking bytes...")
    idx = html.find('var isCollapsed = (dk === "6')
    exact = html[idx:idx+100]
    with open("_debug.txt", "w", encoding="utf-8") as out:
        out.write(repr(exact))