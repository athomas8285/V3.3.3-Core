c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Find all style related tags
print('<style> at:', c.find('<style'))
print('</style> at:')
i = -1
while True:
    i = c.find('</style>', i+1)
    if i < 0: break
    print(f'  {i}: context={repr(c[i-20:i+15])}')