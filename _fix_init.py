import sys
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    h = f.read()

old = 'openAccordion("accWCMain");\n  if(typeof __DATA!=="undefined"&&__DATA&&__DATA.rating&&__DATA.rating.length>0){renderToday(__DATA.rating);document.getElementById("todaySub").textContent="2026-06-06 | "+__DATA.rating.length+"\u573a";updateTodayOverview({matches:__DATA.rating,date:"2026-06-06"});}else{loadToday();}'
new = 'openAccordion("accWCMain");\n  renderGroupSchedule();'

if old in h:
    h = h.replace(old, new)
    print("Replaced default load")
else:
    # Try finding it differently
    idx = h.find('openAccordion("accWCMain")')
    if idx >= 0:
        print(f"Found at {idx}")
        print(repr(h[idx:idx+400]))
    else:
        print("NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(h)
