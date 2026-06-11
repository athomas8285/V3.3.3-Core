import re
c = open('templates/charts.js', 'r', encoding='utf-8').read()
# Remove single-quoted strings
c = re.sub(chr(39)+'[^'+chr(39)+'\\n]*'+chr(39), '', c)
# Remove double-quoted strings
c = re.sub('"[^"\\n]*"', '', c)
# Remove template literals (backtick)
c = re.sub('[^]*', '', c)
# Remove regex literals (simplified - after // but before end of line)
c = re.sub(r'\/\/.*', '', c)

lines = c.split('\n')
bal_b = 0
bal_p = 0
for l in lines:
    for ch in l:
        if ch in '{}': bal_b += 1 if ch == '{' else -1
        if ch in '()': bal_p += 1 if ch == '(' else -1
print('Braces (no strings):', bal_b)
print('Parens (no strings):', bal_p)
