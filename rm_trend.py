import re
with open(r'D:\V3.3.3-Core\templates\index.html', 'r', encoding='utf-8') as f:
    content = f.read()
content = re.sub(
    r'var trendArrow=ld>=0\?"\\u25b2":"\\u25bc";\n',
    '',
    content
)
with open(r'D:\V3.3.3-Core\templates\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
