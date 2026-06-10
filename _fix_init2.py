import sys
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    h = f.read()

# The HTML stores literal \u573a not the actual char
old = 'openAccordion("accWCMain");\n  if(typeof __DATA!=="undefined"&&__DATA&&__DATA.rating&&__DATA.rating.length>0){renderToday(__DATA.rating);document.getElementById("todaySub").textContent="2026-06-06 | "+__DATA.rating.length+"\\u573a";updateTodayOverview({matches:__DATA.rating,date:"2026-06-06"});}else{loadToday();}'
new = 'openAccordion("accWCMain");\n  renderGroupSchedule();'

if old in h:
    h = h.replace(old, new)
    print("Replaced default load OK")
else:
    print("Pattern still not matching")
    # Debug
    idx = h.find('openAccordion("accWCMain")')
    print(repr(h[idx:idx+250]))

with open(path, "w", encoding="utf-8") as f:
    f.write(h)
