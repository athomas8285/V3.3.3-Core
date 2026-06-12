c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# ===== 1. Replace renderCompletedHistory sidebar =====
s1 = c.find('function renderCompletedHistory(){')
s2 = c.find('function scrollToDateGroup', s1)
sq = chr(39)
new_sidebar = 'function renderCompletedHistory(){\n'
new_sidebar += '  var container = document.getElementById(' + sq + 'historyCompletedMatches' + sq + ');\n'
new_sidebar += '  if(!container) return;\n'
new_sidebar += "  if(typeof __DATA === 'undefined' || !__DATA || !__DATA.info){\n"
new_sidebar += "    container.innerHTML = '<div class=\"sd-loading\">\\u52a0\\u8f7d\\u4e2d...</div>';\n"
new_sidebar += '    return;\n  }\n'
new_sidebar += '  var completedScores = {"\\u5468\\u56db001":"2-0","\\u5468\\u56db002":"2-1"};\n'
new_sidebar += '  var completedHits = {"\\u5468\\u56db001":true,"\\u5468\\u56db002":true};\n'
new_sidebar += '  var total = 0, hitCount = 0;\n'
new_sidebar += '  for(var i = 0; i < __DATA.info.length; i++){\n'
new_sidebar += '    var info = __DATA.info[i];\n'
new_sidebar += "    var t = info.time || '';\n"
new_sidebar += "    var dp = t.length >= 10 ? t.slice(0,10) : '';\n"
new_sidebar += "    var mid = info.id || '';\n"
new_sidebar += "    if(dp === '2026-06-12'){\n"
new_sidebar += '      total++;\n'
new_sidebar += '      if(completedHits[mid]) hitCount++;\n'
new_sidebar += '    }\n'
new_sidebar += '  }\n'
new_sidebar += '  if(total === 0){\n'
new_sidebar += "    container.innerHTML = '<div class=\"hist-empty\" style=\"padding:12px;font-size:12px;color:var(--t3);text-align:center;\">\\u6682\\u65e0\\u5df2\\u7ed3\\u675f\\u7684\\u6bd4\\u8d5b</div>';\n"
new_sidebar += '    return;\n  }\n'
new_sidebar += "  var h = '';\n"
new_sidebar += "  h += '<div class=\"hist-date-item\" onclick=\"scrollToDateGroup()\">';\n"
new_sidebar += "  h += '<span class=\"hd-date\">6\\u670812\\u65e5 \\u5468\\u56db</span>';\n"
new_sidebar += "  h += '<span class=\"hd-stats\">' + hitCount + '/' + total + ' \\u547d\\u4e2d</span>';\n"
new_sidebar += "  h += '<span class=\"hd-arrow\">\\u25b6</span>';\n"
new_sidebar += "  h += '</div>';\n"
new_sidebar += '  container.innerHTML = h;\n'
new_sidebar += "  var msg = document.getElementById('historyRestMessage');\n"
new_sidebar += "  if(msg) msg.style.display = 'none';\n"
new_sidebar += '}\n'
c = c[:s1] + new_sidebar + c[s2:]
print('1. Sidebar replaced')

# ===== 2. Replace scrollToDateGroup =====
s1 = c.find('function scrollToDateGroup(')
bc = 0; fs = False; s2 = s1
for i in range(s1, len(c)):
    if c[i] == '{': bc += 1; fs = True
    elif c[i] == '}':
        bc -= 1
        if fs and bc == 0: s2 = i + 1; break
new_scroll = 'function scrollToDateGroup(){\n'
new_scroll += '  switchNav(' + sq + 'analysis' + sq + ');\n'
new_scroll += '  setTimeout(function(){\n'
new_scroll += '    var els = document.querySelectorAll(' + sq + '.ana-date-label' + sq + ');\n'
new_scroll += '    for(var i = 0; i < els.length; i++){\n'
new_scroll += "      if(els[i].textContent.indexOf('6\\u6708') >= 0 && els[i].textContent.indexOf('12') >= 0){\n"
new_scroll += '        var parent = els[i].closest(' + sq + '.ana-date-group' + sq + ');\n'
new_scroll += '        if(parent){\n'
new_scroll += '          var body = parent.querySelector(' + sq + '.ana-date-body' + sq + ');\n'
new_scroll += '          if(body) body.style.display = ' + sq + 'block' + sq + ';\n'
new_scroll += '          var arrow = parent.querySelector(' + sq + '.ana-date-arrow' + sq + ');\n'
new_scroll += '          if(arrow) arrow.textContent = ' + sq + '\\u25bc' + sq + ';\n'
new_scroll += '          parent.scrollIntoView({behavior:' + sq + 'smooth' + sq + ', block:' + sq + 'start' + sq + '});\n'
new_scroll += '          parent.style.transition = ' + sq + 'background .5s' + sq + ';\n'
new_scroll += '          parent.style.background = ' + sq + 'rgba(0,229,255,.06)' + sq + ';\n'
new_scroll += '          setTimeout(function(){ parent.style.background = ' + sq + sq + '; }, 1500);\n'
new_scroll += '        }\n'
new_scroll += '        break;\n'
new_scroll += '      }\n'
new_scroll += '    }\n'
new_scroll += '  }, 500);\n'
new_scroll += '}\n'
c = c[:s1] + new_scroll + c[s2:]
print('2. scrollToDateGroup replaced')

# ===== 3. Insert toggleDateGroup after scrollToDateGroup =====
ins = c.find('function scrollToDateGroup')
bc = 0; fs = False; ins_end = ins
for i in range(ins, len(c)):
    if c[i] == '{': bc += 1; fs = True
    elif c[i] == '}':
        bc -= 1
        if fs and bc == 0: ins_end = i + 1; break
toggle_fn = '\nfunction toggleDateGroup(el){\n'
toggle_fn += '  var parent = el.closest(' + sq + '.ana-date-group' + sq + ');\n'
toggle_fn += '  if(!parent) return;\n'
toggle_fn += '  var body = parent.querySelector(' + sq + '.ana-date-body' + sq + ');\n'
toggle_fn += '  var arrow = parent.querySelector(' + sq + '.ana-date-arrow' + sq + ');\n'
toggle_fn += '  if(!body) return;\n'
toggle_fn += "  if(body.style.display === 'none' || body.style.display === ''){\n"
toggle_fn += '    body.style.display = ' + sq + 'block' + sq + ';\n'
toggle_fn += '    if(arrow) arrow.textContent = ' + sq + '\\u25bc' + sq + ';\n'
toggle_fn += '  } else {\n'
toggle_fn += '    body.style.display = ' + sq + 'none' + sq + ';\n'
toggle_fn += '    if(arrow) arrow.textContent = ' + sq + '\\u25b6' + sq + ';\n'
toggle_fn += '  }\n'
toggle_fn += '}\n'
c = c[:ins_end] + toggle_fn + c[ins_end:]
print('3. toggleDateGroup added')

# ===== 4. Remove 06-12 skip in renderFromData =====
skip = "if(infoDatePart === '2026-06-12') continue;"
idx = c.find(skip)
if idx >= 0:
    ls = c.rfind(chr(10), 0, idx) + 1
    le = c.find(chr(10), idx)
    c = c[:ls] + c[le+1:]
    print('4. 06-12 skip removed')

# ===== 5. Make first date group collapsible =====
rd = c.find('function renderFromData(){')
fd = c.find('for(var di = 0; di < dateKeys.length; di++)', rd)
eh = c.find('el.innerHTML = h;', fd)
fg = c.find('<div class=\"ana-date-group\">', fd)
ng = c.find('<div class=\"ana-date-group\">', fg + 10)
if ng < 0 or ng > eh:
    ng = eh
lm = '<div class=\"ana-date-label\"'
ls = c.find(lm, fg)
le = c.find('</div>', ls) + len('</div>')
old_label = c[ls:le]
new_label = old_label.replace(
    '<div class=\"ana-date-label\"',
    '<div class=\"ana-date-label\" onclick=\"toggleDateGroup(this)\" style=\"cursor:pointer;\"'
)
d = chr(45) + chr(45)
new_label = new_label.replace(
    '</div>',
    '<span class=\"ana-date-arrow\" style=\"margin-left:8px;font-size:10px;color:var(' + d + 't3);\">\\u25b6</span></div><div class=\"ana-date-body\" style=\"display:none;\">'
)
c = c[:ls] + new_label + c[le:]
# Add body close before group close
gc = c.rfind('</div>', fg, ng)
c = c[:gc] + '</div>' + c[gc:]
print('5. First date group made collapsible')

# ===== 6. Remove duplicate disclaimer after footer =====
dup = c.find('<!-- \\u514d\\u8d23\\u58f0\\u660e -->')
fe = c.find('</footer>') + len('</footer>')
if dup > fe:
    e1 = c.find('</div>', dup + 200)
    e2 = c.find('</div>', e1 + 1)
    e3 = c.find('</div>', e2 + 1)
    c = c[:dup] + c[e3+6:]
    print('6. Duplicate disclaimer removed')
else:
    print('6. No duplicate disclaimer found after footer')

open('D:/V3.3.3-Core/templates/index.html', 'w', encoding='utf-8').write(c)
print('ALL DONE!')