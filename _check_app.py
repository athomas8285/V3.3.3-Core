f = open('D:/V3.3.3-Core/app.py', 'r', encoding='utf-8')
c = f.read()
f.close()
print('render_template:', c.count('render_template'))
print('index.html:', c.count('index.html'))
print('templates:', c.count('templates'))
# Find the route that serves the main page
for line in c.split('\n'):
    if 'index.html' in line:
        print('  LINE:', line.strip()[:120])
    if 'render_template' in line:
        print('  RENDER:', line.strip()[:120])
