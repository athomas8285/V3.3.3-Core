c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

print('File size:', len(c))
print('<body> count:', c.count('<body'))
print('</body> count:', c.count('</body>'))
print('</html> count:', c.count('</html>'))
print('<script> count:', c.count('<script'))
print('</script> count:', c.count('</script>'))

# Check sidebar
print()
print('Sidebar renderCompletedHistory:', 'function renderCompletedHistory' in c)
print('06-13 in sidebar:', '6\\u670813' not in c[c.find('function renderCompletedHistory'):c.find('function scrollToDateGroup')])

# Check functions
print('scrollToDateGroup count:', c.count('function scrollToDateGroup'))
print('toggleDateGroup count:', c.count('function toggleDateGroup'))

# Check 06-12 skip
print('06-12 skip:', '06-12' + chr(39) + ') continue;' in c)

# Check collapsible
print('Has onclick label:', 'toggleDateGroup(this)' in c)
print('Has body wrapper:', 'ana-date-body' in c)