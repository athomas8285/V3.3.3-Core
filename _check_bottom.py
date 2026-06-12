c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Look at the page structure near the bottom
# Find the last few HTML structural elements
body_close = c.rfind('</body>')
html_close = c.rfind('</html>')
print('</body> at:', body_close)
print('</html> at:', html_close)

# What's between </footer> and </body>?
fe = c.rfind('</footer>')
between = c[fe+9:body_close]
print()
print('Between footer and body_close (first 100):', repr(between[:100]))
print('Between footer and body_close (last 100):', repr(between[-100:]))