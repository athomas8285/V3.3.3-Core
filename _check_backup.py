c = open('D:/V3.3.3-Core/templates/index.html.bak3', 'r', encoding='utf-8').read()
print('Backup file size:', len(c))
# Check for duplicate structure
i = c.find('</html>')
print('First </html> at:', i)
j = c.find('</html>', i+1)
if j >= 0:
    print('Second </html> at:', j)
    print('Context:', repr(c[i:i+200]))
else:
    print('Only one </html>')
    
# Check body count
print('<body> count:', c.count('<body'))
print('</body> count:', c.count('</body>'))
print('</html> count:', c.count('</html>'))