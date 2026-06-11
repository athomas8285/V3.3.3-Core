import re, os

content = open('D:\\V3.3.3-Core\\templates\\index.html', 'r', encoding='utf-8').read()

# Find function boundaries
idx = content.find('function renderGroupSchedule()')
after_html = content.find('document.getElementById("todayMatches").innerHTML = h;', idx)
print(f"Function start: {idx}, innerHTML line: {after_html}")
# Show content from innerHTML line to +200 chars
snippet = content[after_html:after_html+200]
print(repr(snippet))
