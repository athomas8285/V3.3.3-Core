c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Find the </head> position
hi = c.find('</head>')
print('</head> at:', hi)

# Find <html> start
hs = c.find('<html')
print('<html> at:', hs)

# Check what's between <html> and first <body>
b1 = c.find('<body', 67000)
print('First <body> at:', b1)
if b1 > hs:
    # What's between them?
    between = c[hs:b1]
    print('Between html and first body (first 300):', repr(between[:300]))
    print('Between html and first body (last 100):', repr(between[-100:]))