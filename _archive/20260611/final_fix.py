
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/gjj/Desktop/v333/templates/index.html.codex_bak','r',encoding='utf-8') as f:
    bak = f.read()

with open('C:/Users/gjj/Desktop/v333/templates/index.html','r',encoding='utf-8') as f:
    cur = f.read()

# Extract ALL clean text blocks from backup with their position
# Strategy: find each text block between > and <, keep the longest ones
blocks = []
for m in re.finditer('>([^<]{15,})<', bak):
    t = m.group(1).strip()
    if t and any(ord(c)>0x2FFF for c in t):
        blocks.append(t)

# Sort by length descending, keep unique
blocks = sorted(set(blocks), key=len, reverse=True)

result = cur
changed = 0

for txt in blocks:
    if len(txt) < 20:
        continue
    if txt in result:
        continue
    
    # Check if the corrupted version exists
    # Find first 6 chars of clean text
    sig = txt[:6]
    if sig in result:
        idx = result.find(sig)
        
        # Try to find the corrupted segment by looking for the NEXT sig-like marker
        # The corrupted version likely has the SAME START but then garbled content
        # followed by the same CONTINUATION
        
        # Strategy: find the first 6 chars, then try to match the LAST 6 chars
        end_sig = txt[-6:]
        end_idx = result.find(end_sig, idx + 6)
        
        if end_idx > idx:
            # Found start and end markers - replace the whole segment
            segment = result[idx:end_idx+6]
            result = result[:idx] + txt + result[end_idx+6:]
            changed += 1
            continue
    
    # Try shorter sig
    sig = txt[:5]
    if sig in result:
        end_sig = txt[-5:]
        idx = result.find(sig)
        end_idx = result.find(end_sig, idx + 5)
        if end_idx > idx:
            segment = result[idx:end_idx+5]
            result = result[:idx] + txt + result[end_idx+5:]
            changed += 1

print(f'Changed: {changed}')

# Check remaining issues in right panel
idx = result.find('spPanel')
section = result[idx:idx+8000]
for m in re.finditer('>([^<]{40,})<', section):
    t = m.group(1).strip()
    if any(ord(c)>0x2FFF for c in t):
        if len(t) > 50 and t not in blocks:
            print('STILL BROKEN:', repr(t[:80]))

with open('C:/Users/gjj/Desktop/v333/templates/index.html','w',encoding='utf-8') as f:
    f.write(result)
print('Saved')
