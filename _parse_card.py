content = open('D:/V3.3.3-Core/_railway_card_snippet.txt', 'rb').read().decode('utf-8', errors='replace')
idx = content.find('class="card ')
if idx < 0:
    idx = content.find('grid-layout-row')
if idx > 0:
    print(content[idx:idx+1200])
else:
    print("Not found, printing first 500 chars:")
    print(content[:500])
