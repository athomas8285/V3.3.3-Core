c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Count all script open/close tags
open_script = c.count('<script')
close_script = c.count('</script>')
print(f'Script tags: {open_script} open, {close_script} close')

# Let me check each script section by finding positions
pos = 0
for i in range(open_script):
    s = c.find('<script', pos)
    e = c.find('</script>', s)
    if e < 0:
        print(f'  [{i}] OPEN at {s} - NO CLOSING TAG!')
        print(f'    First 100:', repr(c[s:s+100]))
        break
    else:
        print(f'  [{i}] {s} to {e+9} (len={e+9-s})')
        pos = e + 9