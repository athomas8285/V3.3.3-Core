with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the renderFromWC date-group loop
old = '''    var isCollapsed = (dk === "6\\u670812\\u65e5");
    h += '<div class="ana-date-group">';
    h += '<div class="ana-date-label clickable" onclick="toggleDateGroup(this)">';
    h += '<span class="ana-date-arrow">' + (isCollapsed ? '\\u25b6' : '\\u25bc') + '</span> \\ud83d\\udcc5 ' + dk + '<span class="adl-count">' + ml.length + ' \\u573a</span></div>';
    h += '<div class="ana-date-body"' + (isCollapsed ? ' style="display:none"' : '') + '>';'''

new = '''    var allDoneWC = ml.every(function(m){ return !!m.result; });
    h += '<div class="ana-date-group">';
    h += '<div class="ana-date-label clickable" onclick="toggleDateGroup(this)">';
    h += '<span class="ana-date-arrow">' + (allDoneWC ? '\\u25b6' : '\\u25bc') + '</span> \\ud83d\\udcc5 ' + dk + '<span class="adl-count">' + ml.length + ' \\u573a</span></div>';
    h += '<div class="ana-date-body"' + (allDoneWC ? ' style="display:none"' : '') + '>';'''

count = html.count(old)
print(f"Found {count} occurrences of old pattern")
if count > 0:
    html = html.replace(old, new)
    with open("D:\\V3.3.3-Core\\templates\\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Replaced successfully")
else:
    print("Pattern not found directly, trying alternate approach")
    # The unicode escapes might differ
    idx = html.find('var isCollapsed = (dk === "6')
    if idx >= 0:
        ctx = html[idx:idx+200]
        with open("_raw_match.txt", "w", encoding="utf-8") as out:
            out.write(ctx)
        print(f"Found at idx {idx}")