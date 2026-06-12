c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Check what's at position 282522 (after first </html>)
print('After first </html>:')
print(repr(c[282518:282560]))

# Check if the CSS text between the first /html and second /style has any style tag
text = c[282522:349354]
print(f'\\nText between /html and second /style: {len(text)} chars')
st = text.find('<style')
if st >= 0:
    print(f'Has <style> at relative position {st}')
else:
    print('No <style> tag found')

# Check what came before this section
print('\\nWhat is at the start of the second block?')
print(repr(text[:100]))