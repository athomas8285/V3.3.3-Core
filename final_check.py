import urllib.request, json, re

# Verify page loads
r = urllib.request.urlopen('http://localhost:5000/', timeout=5)
html = r.read().decode('utf-8')

# Count occurrences of chart-lambda-004
count = html.count('chart-lambda-004')
print('chart-lambda-004 occurrences:', count)

# Find each occurrence
for i, m in enumerate(re.finditer(r'.{80}chart-lambda-004.{80}', html)):
    print('--- Occurrence', i+1, '---')
    print(m.group()[:120] + '...')

# Check JS syntax: all braces balanced? 
braces = sum(1 for c in html if c == '{')
br_close = sum(1 for c in html if c == '}')
p_open = sum(1 for c in html if c == '(')
p_close = sum(1 for c in html if c == ')')
print()
print('Braces: {}=%d, }=%d, balanced=%s' % (braces, br_close, braces==br_close))
print('Parens: ()=%d, )=%d, balanced=%s' % (p_open, p_close, p_open==p_close))

# Check API
r2 = urllib.request.urlopen('http://localhost:5000/api/latest', timeout=5)
data = json.loads(r2.read().decode('utf-8'))
print('API rating count:', len(data['rating']))
print('API match 004 direction:', [m['direction'] for m in data['rating'] if m['id']=='004'][0])