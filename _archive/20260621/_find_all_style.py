c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Find ALL <style tags
i = -1
while True:
    i = c.find('<style', i+1)
    if i < 0:
        break
    print(f'<style at {i}: context={repr(c[i:i+30])}')
    # Find matching </style>
    j = c.find('</style>', i)
    if j >= 0:
        print(f'  closes at {j}, len={j-i}')