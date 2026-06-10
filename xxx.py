path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

search_for = '</div></div>'
idx = content.find(search_for, 13500)
print("Found at", idx)
if idx >= 0:
    print("Context:", repr(content[idx-30:idx+80]))