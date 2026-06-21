c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

print('Size:', len(c))
print('body:', c.count('<body'), '/body:', c.count('</body>'))
print('html:', c.count('<html'), '/html:', c.count('</html>'))
print('script:', c.count('<script'), '/script:', c.count('</script>'))
print('div diff:', c.count('<div')-c.count('</div>'))
print()
print('scrollToDateGroup count:', c.count('function scrollToDateGroup'))
print('toggleDateGroup count:', c.count('function toggleDateGroup'))
print('No old label:', 'scrollToDateGroup(label)' not in c)
print('Has 06-12 skip:', '06-12' + chr(39) + ') continue;' in c)
print('Collapsible onclick:', 'toggleDateGroup(this)' in c)
print('ana-date-body:', 'ana-date-body' in c)
print('06-13 in sidebar:', '6\u670813' not in c[c.find('function renderCompletedHistory'):c.find('function scrollToDateGroup')])

# Check the file actually loads
import urllib.request
try:
    r = urllib.request.urlopen('http://localhost:5020/', timeout=5)
    print('Server:', r.status)
except Exception as e:
    print('Server error:', e)