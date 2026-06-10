import os

file = r'D:\V3.3.3-Core\templates\index.html'
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

back_btn = '<button class="sec-back-btn" onclick="switchNav(\'home\')">\u2190 \u8fd4\u56de\u9996\u9875</button>'

# 1. Add back button after each <div class="sec-header"> (for schedule, bracket, odds, top)
# We need to be careful not to add it to the standings header which is in JS
# Find each sec-header that is in static HTML (not JS)
lines = content.split('\n')
new_lines = []
for line in lines:
    stripped = line.strip()
    if stripped == '<div class="sec-header">':
        new_lines.append(line)
        new_lines.append('      ' + back_btn)
    else:
        new_lines.append(line)

content = '\n'.join(new_lines)

# 2. Modify renderStandings() header to include back button
old_standings_header = '<div class="gs-header"><h2>\u5c0f\u7ec4\u79ef\u5206\u699c</h2><div class="gs-bar"></div></div>'
new_standings_header = '<div class="gs-header">' + back_btn + '<h2>\u5c0f\u7ec4\u79ef\u5206\u699c</h2><div class="gs-bar"></div></div>'
content = content.replace(old_standings_header, new_standings_header)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
