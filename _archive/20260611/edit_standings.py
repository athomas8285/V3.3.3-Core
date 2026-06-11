import os

path = r"D:\V3.3.3-Core\templates\index.html"
with open(path, "r", encoding="utf-8-sig") as f:
    c = f.read()

i = c.find("function renderStandings()")
j = c.find("function renderBracket()", i)
if i < 0 or j < 0:
    print("ERROR: markers not found")
    exit(1)

# Read the JS replacement from a separate file
js_path = r"D:\V3.3.3-Core\standings_js_replacement.txt"
with open(js_path, "r", encoding="utf-8") as f:
    new_js = f.read()

c = c[:i] + new_js + c[j:]
with open(path, "w", encoding="utf-8-sig") as f:
    f.write(c)

print(f"Successfully replaced JS from pos {i} to {j}")
