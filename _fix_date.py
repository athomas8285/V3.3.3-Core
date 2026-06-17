import re
with open("D:/V3.3.3-Core/templates/index.html","r",encoding="utf-8") as f:
    content = f.read()

old = 'var isFutureDate = datePart > "2026-06-17";'
new = 'var isFutureDate = datePart > "2026-06-18";'

if old in content:
    content = content.replace(old, new)
    with open("D:/V3.3.3-Core/templates/index.html","w",encoding="utf-8") as f:
        f.write(content)
    print("Fixed: isFutureDate updated to 2026-06-18")
else:
    print("Not found - checking for current value...")
    for line in content.split("\n"):
        if "isFutureDate" in line:
            print(f"  Found: {line.strip()[:80]}")
