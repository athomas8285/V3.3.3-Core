import re
with open("index.html","r",encoding="utf-8") as f:
    t = f.read()
m = re.search(r'<div class="sp" id="spPanel">(.*?)<script', t, re.DOTALL)
if m:
    print(m.group(1))
else:
    print("NOT FOUND")
