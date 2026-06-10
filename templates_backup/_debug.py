import re
BASE = "C:/Users/gjj/Desktop/v333/templates"
with open(BASE + "/index.html.codex_bak", "r", encoding="utf-8") as f:
    bak = f.read()

sp_l_start = bak.index('<div class="sp-l" id="spLPanel">')
sp_l_end = bak.index('<div class="sp-wrap" id="spWrap">')
lhtml = bak[sp_l_start:sp_l_end]

# Return div balance for sections
def bal(s): return f"{s.count('<div')}O/{s.count('</div>')}C"

# intro
intro_m = re.search(
    r'<div class="meth">\s*<div class="meth-h">分析系统介绍</div>(.*?)(?=</div>\s*<div class="meth">|</div>\s*<div style=)',
    lhtml, re.DOTALL
)
intro = intro_m.group(1) if intro_m else ""
print(f"intro: {bal(intro)}")

# version
ver_m = re.search(
    r'<div style="margin-top:20px;padding-top:16px;border-top:2px solid var\(--bd\)">(.*?)</div>\s*</div>\s*</div>',
    lhtml, re.DOTALL
)
ver = ver_m.group(1) if ver_m else ""
print(f"ver: {bal(ver)}")

# param_bd
sp_p_start = bak.index('<div class="sp" id="spPanel">')
sp_p_end = bak.index('<script src="/charts.js"></script>', sp_p_start)
ph = bak[sp_p_start:sp_p_end]
pbd_m = re.search(r'<div class="sp-bd">(.*?)</div>\s*$', ph, re.DOTALL)
pbd = pbd_m.group(1) if pbd_m else ""
print(f"pbd: {bal(pbd)}")

# Also check the original current_fix spPanel
with open(BASE + "/index.html.current_fix", "r", encoding="utf-8") as f:
    fix = f.read()

sp_start = fix.index('<div class="sp" id="spPanel">')
sc_end = fix.index('<script src="/charts.js">', sp_start)
old_panel = fix[sp_start:sc_end]
print(f"old_panel: {bal(old_panel)}")
