# Check app.py for the right place to add a route
import re
with open("D:/V3.3.3-Core/app.py","r",encoding="utf-8-sig") as f:
    c = f.read()

# Find the last API route
routes = re.findall(r"@app\.route\('[^']+'\)", c)
for r in routes:
    print(r)
print()
# Find where to insert
idx = c.find("if __name__")
print(f"__main__ at line: {c[:idx].count(chr(0x0a)) + 1 if idx >= 0 else 'N/A'}")

# Show last few routes
last_route = routes[-1] if routes else ""
print(f"Last route: {last_route}")
