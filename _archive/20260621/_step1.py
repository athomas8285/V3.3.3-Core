c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

sq = chr(39)

# Step 1: Replace renderCompletedHistory
s1 = c.find('function renderCompletedHistory(){')
s2 = c.find('function scrollToDateGroup', s1)

new_func = 'function renderCompletedHistory(){\n'
new_func += '  var container = document.getElementById(' + sq + 'historyCompletedMatches' + sq + ');\n'
new_func += '  if(!container) return;\n'
new_func += "  if(typeof __DATA === 'undefined' || !__DATA || !__DATA.info){\n"
new_func += "    container.innerHTML = '<div class=\"sd-loading\">\u52a0\u8f7d\u4e2d...</div>';\n"
new_func += '    return;\n  }\n'
new_func += '  var completedScores = {\u0022\u5468\u56db001\u0022:\u00222-0\u0022,\u0022\u5468\u56db002\u0022:\u00222-1\u0022};\n'
new_func += '  var completedHits = {\u0022\u5468\u56db001\u0022:true,\u0022\u5468\u56db002\u0022:true};\n'
new_func += '  var total = 0, hitCount = 0;\n'
new_func += '  for(var i = 0; i < __DATA.info.length; i++){\n'
new_func += '    var info = __DATA.info[i];\n'
new_func += "    var t = info.time || '';\n"
new_func += "    var dp = t.length >= 10 ? t.slice(0,10) : '';\n"
new_func += "    var mid = info.id || '';\n"
new_func += "    if(dp === '2026-06-12'){\n"
new_func += '      total++;\n'
new_func += '      if(completedHits[mid]) hitCount++;\n'
new_func += '    }\n'
new_func += '  }\n'
new_func += '  if(total === 0){\n'
new_func += "    container.innerHTML = '<div class=\"hist-empty\" style=\"padding:12px;font-size:12px;color:var(--t3);text-align:center;\">\u6682\u65e0\u5df2\u7ed3\u675f\u7684\u6bd4\u8d5b</div>';\n"
new_func += '    return;\n  }\n'
new_func += "  var h = '';\n"
new_func += "  h += '<div class=\"hist-date-item\" onclick=\"scrollToDateGroup()\">';\n"
new_func += "  h += '<span class=\"hd-date\">6\u670812\u65e5 \u5468\u56db</span>';\n"
new_func += "  h += '<span class=\"hd-stats\">' + hitCount + '/' + total + ' \u547d\u4e2d</span>';\n"
new_func += "  h += '<span class=\"hd-arrow\">\u25b6</span>';\n"
new_func += "  h += '</div>';\n"
new_func += '  container.innerHTML = h;\n'
new_func += "  var msg = document.getElementById('historyRestMessage');\n"
new_func += "  if(msg) msg.style.display = 'none';\n"
new_func += '}\n'

c = c[:s1] + new_func + c[s2:]
open('D:/V3.3.3-Core/templates/index.html', 'w', encoding='utf-8').write(c)
print('Step 1 done:', len(c))