
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/gjj/Desktop/v333/templates/index.html','r',encoding='utf-8') as f:
    c = f.read()
idx = c.find('spPanel')
print('spPanel at:', idx)
if idx >= 0:
    # Find the sp-bd section
    bd = c.find('sp-bd', idx)
    print('sp-bd at:', bd)
    # Find the matching closing div for the sp-bd
    div = c.rfind('<div', 0, bd)
    print('div at:', div)
    # Simple depth counting from div
    depth = 0
    pos = div
    while pos < len(c):
        if c[pos:pos+4] == '<div' and c[pos+4] != '/':
            depth += 1
            pos += 4
        elif c[pos:pos+6] == '</div>':
            depth -= 1
            pos += 6
            if depth == 0:
                print('Section end at:', pos)
                print('Section length:', pos-div)
                # Print key sections
                section = c[div:pos]
                for kw in ['分析框架', '框架参数说明', 'sp-g-tl', 'sp-g-h']:
                    print(f'{kw}: {section.count(kw)}')
                break
        else:
            pos += 1
