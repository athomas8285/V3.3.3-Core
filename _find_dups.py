c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Find all <body occurrences
i = -1
while True:
    i = c.find('<body', i+1)
    if i < 0: break
    ctx = c[i:i+40]
    print(f'<body at {i}: {repr(ctx)}')

print()
i = -1
while True:
    i = c.find('</body>', i+1)
    if i < 0: break
    ctx = c[i-5:i+10]
    print(f'</body> at {i}: {repr(ctx)}')

print()
i = -1
while True:
    i = c.find('</html>', i+1)
    if i < 0: break
    ctx = c[i-5:i+10]
    print(f'</html> at {i}: {repr(ctx)}')