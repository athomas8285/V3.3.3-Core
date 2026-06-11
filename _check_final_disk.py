f = open('D:/V3.3.3-Core/templates/index.html', 'rb')
d = f.read()
f.close()

# Check disclaimer
idx = d.find(b'ft-disclaimer')
print('Disclaimer at byte:', idx)

# Check if emoji is actual bytes
check = d[idx:idx+250]
if b'\\u26a0' in check:
    print('FAIL: literal backslash-u escape')
else:
    print('OK: Unicode chars correctly encoded')
    
# Check if disclaimer is before script
script_idx = d.find(b'<script>', 68000)
print('Script at byte:', script_idx)
print('Disclaimer before script:', idx < script_idx)

# Show sample
print('Sample:', check[:150])
