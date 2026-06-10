import re

BASE = "C:/Users/gjj/Desktop/v333/templates"

with open(BASE + "/index.html.codex_bak", "r", encoding="utf-8") as f:
    bak = f.read()

with open(BASE + "/index.html.current_fix", "r", encoding="utf-8") as f:
    fix = f.read()

# Extract left panel content
sp_l_start = bak.index('<div class="sp-l" id="spLPanel">')
sp_l_end = bak.index('<div class="sp-wrap" id="spWrap">')
left_panel_html = bak[sp_l_start:sp_l_end]

# Extract intro section
intro_pattern = re.compile(
    r'<div class="meth">\s*<div class="meth-h">分析系统介绍</div>(.*?)(?=</div>\s*<div class="meth">|</div>\s*<div style=)',
    re.DOTALL
)
intro_m = intro_pattern.search(left_panel_html)
intro_html = intro_m.group(1) if intro_m else ""

def extract_meth(html, name):
    pattern = re.compile(
        r'<div class="meth">\s*<div class="meth-h">' + re.escape(name) + r'</div>\s*<div class="meth-p">(.*?)</div>\s*</div>',
        re.DOTALL
    )
    m = pattern.search(html)
    return m.group(1).strip() if m else ""

core_logic = extract_meth(left_panel_html, "核心逻辑")
lambda_calc = extract_meth(left_panel_html, "Lambda 计算")
ddi_calib = extract_meth(left_panel_html, "DDI 校准")
factor_fix = extract_meth(left_panel_html, "因子修正")
risk_ctrl = extract_meth(left_panel_html, "风控降级")

# Extract version history
ver_pattern = re.compile(
    r'<div style="margin-top:20px;padding-top:16px;border-top:2px solid var\(--bd\)">(.*?)</div>\s*</div>\s*</div>',
    re.DOTALL
)
ver_m = ver_pattern.search(left_panel_html)
ver_html = ver_m.group(1) if ver_m else ""

# Extract param descriptions from backup spPanel
sp_panel_start = bak.index('<div class="sp" id="spPanel">')
sp_panel_end = bak.index('<script src="/charts.js"></script>', sp_panel_start)
param_html = bak[sp_panel_start:sp_panel_end]
param_bd_pattern = re.compile(r'<div class="sp-bd">(.*?)</div>\s*$', re.DOTALL)
param_bd_m = param_bd_pattern.search(param_html)
param_bd = param_bd_m.group(1) if param_bd_m else ""

# Build collapsible sections
def make_sp_g(title, content):
    esc_title = title.replace("'", "\\'")
    return f"""      <div class="sp-g">
        <div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){{c.classList.toggle('open');p.classList.toggle('expanded');}}">{title}</div>
        <div class="sp-g-c">{content}</div>
      </div>"""

def make_meth_p(text):
    return f'<div class="meth-p">{text}</div>'

# Section 1
sec1_content = ""
sec1_content += make_sp_g("分析系统介绍", intro_html)
sec1_content += make_sp_g("核心逻辑", make_meth_p(core_logic))
sec1_content += make_sp_g("Lambda 计算", make_meth_p(lambda_calc))
sec1_content += make_sp_g("DDI 校准", make_meth_p(ddi_calib))
sec1_content += make_sp_g("因子修正", make_meth_p(factor_fix))
sec1_content += make_sp_g("风控降级", make_meth_p(risk_ctrl))
sec1_content += make_sp_g("版本更新", ver_html)

section1 = f"""  <div class="sp-g sp-g-tl">
    <div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){{c.classList.toggle('open');p.classList.toggle('expanded');}}">V3.3.3-Core 分析框架</div>
    <div class="sp-g-c">
{sec1_content}
    </div>
  </div>"""

# Section 2
section2 = f"""  <div class="sp-g sp-g-tl">
    <div class="sp-g-h" onclick="var p=this.parentNode;var c=p.querySelector('.sp-g-c');if(c){{c.classList.toggle('open');p.classList.toggle('expanded');}}">框架参数说明</div>
    <div class="sp-g-c">
{param_bd}
    </div>
  </div>"""

new_right_panel = f"""<div class="sp" id="spPanel"><div class="sp-hdr"><h2>V3.3.3-Core 分析框架</h2></div>
<div class="sp-bd">
{section1}
{section2}
</div>
</div>"""

# Verify div balance
open_divs = new_right_panel.count("<div")
close_divs = new_right_panel.count("</div>")
print(f"New panel: {open_divs} open, {close_divs} close, diff={open_divs-close_divs}")

# Find region to replace
sp_start = fix.index('<div class="sp" id="spPanel">')
script_marker = '<script src="/charts.js">'
script_pos = fix.index(script_marker, sp_start)
before_script = fix[sp_start:script_pos]

# Find the last </div> (closes sp), consume both close divs (sp-bd + sp)
# We need to find the last two </div> before script_marker
last_close = before_script.rstrip().rfind("</div>")
# After last_close + 6 (= len("</div>")), that's right after </div> which closes sp
sp_end = sp_start + last_close + 6

print(f"Replacing range: {sp_start} to {sp_end}")
print(f"Old length: {sp_end - sp_start}")
print(f"New length: {len(new_right_panel)}")

# Replace
new_fix = fix[:sp_start] + new_right_panel + fix[sp_end:]

# Fix CSS margin
new_fix = new_fix.replace("margin:0 auto", "margin:0 80px 0 40px")

# Verify total balance
total_open = new_fix.count("<div")
total_close = new_fix.count("</div>")
print(f"Total file: {total_open} open, {total_close} close, diff={total_open-total_close}")
print(f"Original: {len(fix)} bytes -> New: {len(new_fix)} bytes")

# Verify the spPanel section ends right before the script tag
sp_new = new_fix.index('<div class="sp" id="spPanel">')
sc_new = new_fix.index('<script src="/charts.js">', sp_new)
after_panel = new_fix[sp_new:sc_new]
print(f"Panel ends with: ...{after_panel[-60:]}")

with open(BASE + "/index.html", "w", encoding="utf-8") as f:
    f.write(new_fix)
print("DONE")
