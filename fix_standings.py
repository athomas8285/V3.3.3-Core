path = r'D:\V3.3.3-Core\templates\index.html'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

print('=== renderStandings function ===')
for i in range(1448, 1475):
    if i < len(lines):
        try:
            print(f'{i+1}: {lines[i].rstrip()}')
        except:
            print(f'{i+1}: [unicode]')