c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()
# Check around the footer area
fe = c.rfind('</footer>')
after = c[fe:fe+300]
print(repr(after))