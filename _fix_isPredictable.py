c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()
sq = chr(39)
old = "var isPredictable = datePart === '2026-06-13';"
new_s = "var isPredictable = datePart === '2026-06-13'" + ' ' + chr(124)*2 + " datePart === '2026-06-12';"
c = c.replace(old, new_s)
open('D:/V3.3.3-Core/templates/index.html', 'w', encoding='utf-8').write(c)
print('isPredictable updated')