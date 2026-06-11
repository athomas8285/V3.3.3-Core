f = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8')
c = f.read()
f.close()

# Find main div and closing structure
idx = c.find('class="main"')
print(f'Main div opens at char: {idx}')
print(f'Context: ...{c[idx-20:idx+50]}...')

# Find where disclaimer sits relative to any parent divs
dc_idx = c.find('ft-disclaimer')
print(f'Disclaimer at char: {dc_idx}')

# Check if there is a </div> closing the main before the disclaimer
# Find the last </div> that could close .main
last_div = c.rfind('</div>', 0, dc_idx)
print(f'Last </div> before disclaimer: {last_div}')
print(f'Text around it: {c[max(0,last_div-30):last_div+30]}')
