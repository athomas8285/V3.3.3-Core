c = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8').read()

# Find all script sections after the last </footer>
fe = c.rfind('</footer>')
after = c[fe:]

# Find all <script> and </script> pairs
import re
scripts = [(m.start()-fe, m.group()) for m in re.finditer(r'<script[^>]*>.*?</script>', after, re.DOTALL)]
print('Script sections after footer:')
for pos, tag in scripts:
    print(f'  at +{pos}: <script...> (len={len(tag)})')

# Check if there's any non-script content between footer and /body
script_end = 0
for pos, tag in scripts:
    end = pos + len(tag)
    if end > script_end:
        script_end = end

non_script = after[script_end:]
if non_script.strip():
    print('Non-script content after footer:', repr(non_script[:200]))
else:
    print('All clean after footer')