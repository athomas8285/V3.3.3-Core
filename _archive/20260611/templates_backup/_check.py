f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "r", encoding="utf-8")
c = f.read()
f.close()
sp = c.index("<div class=\"sp\" id=\"spPanel\">")
before = c[:sp]
print("Before spPanel divs:", before.count("<div"), "open,", before.count("</div>"), "close")
# find closing element before spPanel
print("Last 300 chars before spPanel:", repr(before[-300:]))
