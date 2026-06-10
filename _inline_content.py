import re

with open(r'D:\V3.3.3-Core\_params_html.txt', 'r', encoding='utf-8') as f:
    params_html = f.read()
with open(r'D:\V3.3.3-Core\_framework_html.txt', 'r', encoding='utf-8') as f:
    framework_html = f.read()

with open(r'D:\V3.3.3-Core\templates\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Insert content constants after TEAM_FLAGS
insert_marker = 'var TEAM_FLAGS = {'
idx = html.find(insert_marker)
if idx >= 0:
    end_of_flags = html.find('};', idx)
    if end_of_flags >= 0:
        end_of_line = html.find('\n', end_of_flags)
        constants = '\n// ====== \u7cfb\u7edf\u8bf4\u660e\u4e66\u5185\u5bb9\u5e38\u91cf ======\n'
        constants += 'var DOC_CONTENT = {};\n'
        constants += 'DOC_CONTENT["params"] = `' + params_html + '`;\n'
        constants += 'DOC_CONTENT["framework"] = `' + framework_html + '`;\n'
        html = html[:end_of_line+1] + constants + html[end_of_line+1:]

# Replace showDocContent
old_func = 'function showDocContent(type, title){\n  document.querySelectorAll'
new_func = 'function showDocContent(type, title){\n  document.querySelectorAll(\'.view-content\').forEach(function(el){ el.style.display = \'none\'; });\n  var dc = document.getElementById("docContent");\n  if(dc) dc.style.display = "block";\n  var inner = document.getElementById("docInner");\n  if(!inner) return;\n  if(document.querySelector(\'.main\')) document.querySelector(\'.main\').scrollTop = 0;\n  var key = type === \'params\' ? \'params\' : \'framework\';\n  var content = DOC_CONTENT[key] || \'<div class="doc-error">\u5185\u5bb9\u672a\u627e\u5230</div>\';\n  var backBtn = \'<div class="doc-back-bar">\' +\n    \'<button class="doc-back-btn" onclick="switchNav(\\\'home\\\')">\u2190 \u8fd4\u56de\u9996\u9875</button>\' +\n    \'<span class="doc-current-title">\' + title + \'</span></div>\';\n  inner.innerHTML = backBtn + \'<div class="doc-body">\' + content + \'</div>\';\n}'

idx2 = html.find(old_func)
if idx2 >= 0:
    # Find the closing brace of the function
    brace_count = 0
    start = idx2
    for i in range(start, len(html)):
        if html[i] == '{':
            brace_count += 1
        elif html[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break
    html = html[:idx2] + new_func + html[end:]

with open(r'D:\V3.3.3-Core\templates\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done')
