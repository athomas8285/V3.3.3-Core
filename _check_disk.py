f = open('D:/V3.3.3-Core/templates/index.html', 'rb')
d = f.read()
f.close()
print('Size:', len(d))
idx = d.find(b'ft-disclaimer')
if idx < d.find(b'71652'):  # after the disclaimer before the script
    print('PASS: Disclaimer is before script')
else:
    print('FAIL: Disclaimer is after script')
# Check for backslash-u literal
check = d[idx:idx+200]
if b'\\u26a0' in check:
    print('WARN: Has literal \\u escape (will show as text, not emoji)')
    print('  sample:', check[:100])
else:
    print('OK: Unicode chars are properly encoded')
