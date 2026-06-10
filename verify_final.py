python -c "
with open(r'C:\Users\gjj\Desktop\v333\templates\v4.html','r',encoding='utf-8') as f:
    lines = f.readlines()

print('=== 侧边栏 HTML ===')
for i,l in enumerate(lines):
    if any(x in l for x in ['sidebar-section','date-list','historyDateList','sd-logo','sd-wrap']):
        if i < 130:
            print(f'{i}: {l.rstrip()}')

print()
print('=== 新 CSS ===')
for i,l in enumerate(lines):
    if any(x in l for x in ['sidebar-section','date-list','date-item']):
        if 'sd-' not in l:
            print(f'{i}: {l.rstrip()}')

print()
print('=== renderDateList ===')
in_func = False
for i,l in enumerate(lines):
    if 'function renderDateList' in l:
        in_func = True
    if in_func:
        print(f'{i}: {l.rstrip()}')
        if l.strip() == '}':
            break

print()
print('=== loadToday 开头 ===')
for i,l in enumerate(lines):
    if 'function loadToday()' in l:
        for j in range(i, min(i+5, len(lines))):
            print(f'{j}: {lines[j].rstrip()}')
        break
"'
