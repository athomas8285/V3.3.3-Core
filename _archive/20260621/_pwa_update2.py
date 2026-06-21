content = open("D:/V3.3.3-Core/templates/index.html", "r", encoding="utf-8").read()
old = 'navigator.serviceWorker.register(\"/static/sw.js\")'
new = 'navigator.serviceWorker.register(\"/static/sw.js\",{scope:\"/\"})'
content = content.replace(old, new)
open("D:/V3.3.3-Core/templates/index.html", "w", encoding="utf-8").write(content)
print("scope updated")
