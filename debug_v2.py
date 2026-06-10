content = open('C:\\Users\\gjj\\Desktop\\v333\\templates\\v2.html', 'r', encoding='utf-8', errors='replace').read()
idx = content.find('src=\"/charts.js\"')
print('Around charts.js include:')
print(content[idx:idx+350])
tmp = content[idx:idx+500]
if '</script>' in tmp:
    print('script tags properly closed')
else:
    print('WARNING: script tag may not be properly closed')