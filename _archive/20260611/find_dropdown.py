path = r'C:\Users\gjj\Desktop\v333\templates\charts.js'
with open(path, 'r', encoding='utf-8') as f:
    s = f.read()

# Search for the dropdown close pattern
# The HTML has escaped quotes for onchange: setFilter(\\'rating\\',\\'X\\')
# Let's search for the simpler pattern
idx = s.find("filterDropdown")
print(f"filterDropdown at {idx}")

# Print 200 chars around it
sec = s[idx:idx+600]
print(sec[:400])
