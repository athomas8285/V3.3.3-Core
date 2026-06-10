import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/gjj/Desktop/v333/templates/index.html.current_fix', 'r', encoding='utf-8', errors='replace') as f:
    cur = f.read()

# Extract app tag
app_s = cur.find('<div class=')
# Find the one with 'app' in it
while app_s >= 0:
    app_e = cur.find('>', app_s)
    tag = cur[app_s:app_e+1]
    if 'app' in tag and ('display:flex' in tag or 'max-width' in tag):
        print('APP TAG:', tag)
        break
    app_s = cur.find('<div class=', app_e)

# Extract left panel area
lp_s = cur.find('leftPanel')
if lp_s >= 0:
    # Go back to find the full left panel structure
    # Find the containing div
    start = cur.rfind('<div', 0, lp_s)
    end = cur.find('</div>', lp_s)
    # Find the matching closing div
    depth = 1
    pos = lp_s
    while depth > 0:
        next_open = cur.find('<div', pos+1)
        next_close = cur.find('</div>', pos+1)
        if next_close < next_open or next_open == -1:
            depth -= 1
            pos = next_close + 6
        else:
            depth += 1
            pos = next_open + 1
    
    lp_html = cur[start:pos]
    print()
    print('=== LEFT PANEL HTML ===')
    print(lp_html[:2000])
    # Count bad chars in left panel
    bad = sum(1 for c in lp_html if c == '?' or ord(c) == 0xFFFD)
    print(f'Bad chars in left panel: {bad}')

