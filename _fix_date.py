c = open('D:/V3.3.3-Core/templates/index.html', encoding='utf-8').read()
old = "datePart === '2026-06-12'"
new = "datePart >= '2026-06-12' && datePart <= '2026-06-14'"
c = c.replace(old, new)
open('D:/V3.3.3-Core/templates/index.html', 'w', encoding='utf-8').write(c)
print('Updated')
