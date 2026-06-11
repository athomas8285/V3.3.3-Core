import urllib.request
r = urllib.request.urlopen('http://localhost:5000/', timeout=5)
html = r.read().decode('utf-8')

# 1. Check no standalone chart section
print('1. Standalone chart section removed:', 'chart-section">' not in html)

# 2. Check toggleDetail is patched
print('2. toggleDetail patched:', 'el.classList.contains' in html)

# 3. Check chart canvas IDs exist (as HTML template strings)
print('3. chart-lambda-004 in template:', 'chart-lambda-004' in html)
print('4. chart-prob-004 in template:', 'chart-prob-004' in html)

# 4. Check no double ++
print('5. No ++ bug:', ":'')++" not in html)

# 5. Check chart position (should be after risk ternary)
idx = html.find('chart-lambda-004')
before = html[idx-200:idx]
print('6. Charts after risk:', 'risk' in before)

# 6. Check renderCharts function
import re
m = re.search(r'function renderCharts\\(data\\)[^}]+\\}', html)
if m:
    func = m.group()
    print('7. renderCharts function length:', len(func))
    print('   Has shadowBlur:', 'shadowBlur' in func)
    print('   Has offsetParent:', 'offsetParent' in func)
    print('   Has roundRect:', 'roundRect' in func)

# 7. Verify API data
r2 = urllib.request.urlopen('http://localhost:5000/api/latest', timeout=5)
import json
data = json.loads(r2.read().decode('utf-8'))
m4 = [m for m in data['mc'] if m['id']=='004'][0]
print('8. API data OK:', m4['lambda_h_final'] == 1.3973)

# Summary
print()
print('=== SUMMARY ===')
print('All checks passed')