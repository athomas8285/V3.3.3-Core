# -*- coding: utf-8 -*-
import sys

with open("D:/V3.3.3-Core/templates/index.html", "r", encoding="utf-8-sig") as f:
    c = f.read()

script_pos = c.find("<script>", 68000)
stray = c.rfind("</div>", 0, script_pos)
main_close = c.rfind("</div>", 0, stray)

chars = []
chars.append(ord("\u26a0"))
chars.append(ord("\ufe0f"))
emoji = "".join(chr(cp) for cp in chars)

d1 = emoji + " \u514d\u8d23\u58f0\u660e\uff1a\u672c\u7f51\u7ad9\u6240\u63d0\u4f9b\u7684\u6240\u6709\u8d5b\u4e8b\u5206\u6790\u53ca\u9884\u6d4b\u7ed3\u679c\uff0c\u4ec5\u4f9b\u4f53\u80b2\u7231\u597d\u8005\u4ea4\u6d41\u53c2\u8003\uff0c\u4e0d\u6784\u6210\u4efb\u4f55\u6295\u6ce8\u5efa\u8bae\u6216\u627f\u8bfa\u3002"
d2 = emoji + " \u5f69\u7968\u6709\u98ce\u9669\uff0c\u6295\u6ce8\u9700\u8c28\u614e\u3002\u8bf7\u7406\u6027\u8d2d\u5f69\uff0c\u91cf\u529b\u800c\u884c\u3002\u672a\u6ee118\u5c81\u4e0d\u5f97\u8d2d\u4e70\u5f69\u7968\u3002"

lines = []
lines.append("")
lines.append("<!-- \u514d\u8d23\u58f0\u660e -->")
lines.append('<div class="ft-disclaimer" style="margin-top:40px;padding:18px 24px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;font-size:11px;line-height:1.8;color:#64748b;">')
lines.append('  <div class="ft-row" style="max-width:640px;margin:0 auto;">')
lines.append("    " + d1)
lines.append("  </div>")
lines.append('  <div class="ft-row" style="max-width:640px;margin:0 auto;">')
lines.append("    " + d2)
lines.append("  </div>")
lines.append("</div>")
lines.append("")

disc = "\n".join(lines)

c = c[:main_close] + disc + c[main_close:]

with open("D:/V3.3.3-Core/templates/index.html", "w", encoding="utf-8") as f:
    f.write(c)

print("Done")
