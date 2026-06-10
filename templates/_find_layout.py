f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "r", encoding="utf-8")
c = f.read()
f.close()

# Find the left sidebar container structure
idx = c.find("历史比赛预测查询")
# Go backwards to find the container
before = c[:idx]
# Find the last <div before this
last_div_start = before.rfind("<div")
print("Container starts at:", last_div_start)
print(c[last_div_start:last_div_start+200])
print("===")
# Find closing
after = c[idx:]
# Find where the flex container ends
# Look for the main content area start
main_start = after.find("<hdr>")
if main_start > 0:
    print("Main content starts after:", main_start)
    print(after[:main_start+50])
