import urllib.request
r = urllib.request.urlopen('http://localhost:5000/v2', timeout=5)
content = r.read().decode('utf-8', errors='replace')

# Find the override script section
idx = content.find('window.onload=function')
if idx >= 0:
    # Find the start of this script tag
    script_start = content.rfind('<script', 0, idx)
    # Find the end of this script tag  
    script_end = content.find('</script>', idx)
    full_script = content[script_start:script_end+9]
    print('=== OVERRIDE SCRIPT ===')
    print(full_script)
    print()
    print('Length:', len(full_script))
    print()
    # Check for syntax issues
    if '\\u' in full_script:
        print('Has unicode escapes')
    # Check braces balance
    opens = full_script.count('{')
    closes = full_script.count('}')
    print(f'Braces: {{ = {opens}, }} = {closes}')