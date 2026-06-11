f = open('D:/V3.3.3-Core/templates/index.html', 'rb')
d = f.read()
f.close()
idx = d.find(b'ft-disclaimer')
print('Disclaimer at:', idx)
check = d[idx:idx+200]
if b'\\u' in check:
    print('FAIL: still has literal backslash-u')
else:
    print('OK: no literal backslash-u in disclaimer area')
script_idx = d.find(b'<script>', 68000)
print('Script at:', script_idx)
print('Before script:', idx < script_idx)
# Show the content
import sys
sys.stdout.buffer.write(check[:180] + b'\n')
