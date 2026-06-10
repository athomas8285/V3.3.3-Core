import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

new_styles = """.date-item .d{font-size:13px;font-weight:600}
.date-item.today-item .d{font-size:14px;font-weight:700;color:var(--green)}
.date-item.today-item .s{color:var(--green);font-size:10px}
.date-item.hist-item .d{font-size:12px;font-weight:500;color:var(--t2)}
.date-item.hist-item .s{font-size:10px;color:var(--t3)}
.date-item.hist-item:hover .d{color:var(--t1)}
"""

if ".date-item .d" not in html:
    target = ".today-date{text-shadow:0 0 10px rgba(0,230,118,.15)}"
    html = html.replace(target, new_styles + "\n" + target)
    print("CSS styles added")
else:
    print("CSS styles already present")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)
