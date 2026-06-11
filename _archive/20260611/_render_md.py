import re

def render_md(md):
    if not md:
        return ''
    s = md
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'```(\w*)\n([\s\S]*?)```', lambda m: '<pre style="background:rgba(255,255,255,.04);border:1px solid var(--bd);border-radius:6px;padding:12px 14px;overflow-x:auto;font-size:12px;line-height:1.6;font-family:var(--mono);color:var(--t1);margin:8px 0">' + m.group(2).strip() + '</pre>', s)
    s = re.sub(r'`([^`]+)`', r'<code style="background:rgba(255,255,255,.06);padding:1px 6px;border-radius:3px;font-family:var(--mono);font-size:12px;color:var(--cyan)">\1</code>', s)
    s = re.sub(r'^---+', r'<hr style="border:none;border-top:1px solid var(--bd);margin:16px 0">', s, flags=re.MULTILINE)
    s = re.sub(r'^### (.+)$', r'<h3 style="font-size:15px;font-weight:700;color:var(--gold);margin:16px 0 8px;padding-bottom:4px;border-bottom:1px solid rgba(251,191,36,.12)">\1</h3>', s, flags=re.MULTILINE)
    s = re.sub(r'^## (.+)$', r'<h2 style="font-size:17px;font-weight:700;color:var(--cyan);margin:20px 0 10px;padding-bottom:6px;border-bottom:1px solid rgba(0,229,255,.12)">\1</h2>', s, flags=re.MULTILINE)
    s = re.sub(r'^# (.+)$', r'<h1 style="font-size:20px;font-weight:700;color:var(--t1);margin:20px 0 12px">\1</h1>', s, flags=re.MULTILINE)
    s = re.sub(r'^> (.+)$', r'<div style="background:rgba(0,229,255,.06);border-left:3px solid var(--cyan);padding:6px 12px;margin:8px 0;font-size:12px;color:var(--t2)">\1</div>', s, flags=re.MULTILINE)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color:var(--t1);font-weight:700">\1</strong>', s)
    def fix_table(m):
        rows = m.group(0)
        rows = re.sub(r'\|[-\s:|]+\|', '', rows)
        cells_out = []
        for line in rows.strip().split('\n'):
            line = line.strip()
            if not line or not line.startswith('|'):
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            tds = ''.join('<td style="padding:5px 10px;border:1px solid var(--bd);font-size:12px;color:var(--t2)">'+c+'</td>' for c in cells)
            cells_out.append('<tr>'+tds+'</tr>')
        if cells_out:
            return '<table style="width:100%;border-collapse:collapse;margin:8px 0;font-size:12px"><tbody>'+''.join(cells_out)+'</tbody></table>'
        return ''
    s = re.sub(r'(\|.+\|\n?)+', fix_table, s)
    lines = s.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('<'):
            result.append(line)
        else:
            result.append('<p style="font-size:13px;line-height:1.7;color:var(--t2);margin:6px 0">'+stripped+'</p>')
    return '\n'.join(result)

with open(r'D:\V3.3.3-Core\_doc_params.md', 'r', encoding='utf-8') as f:
    params_md = f.read()
with open(r'D:\V3.3.3-Core\_doc_framework.md', 'r', encoding='utf-8') as f:
    framework_md = f.read()

params_html = render_md(params_md)
framework_html = render_md(framework_md)

def escape_js(s):
    return s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

with open(r'D:\V3.3.3-Core\_params_html.txt', 'w', encoding='utf-8') as f:
    f.write(escape_js(params_html))
with open(r'D:\V3.3.3-Core\_framework_html.txt', 'w', encoding='utf-8') as f:
    f.write(escape_js(framework_html))

print('params_html length:', len(params_html))
print('framework_html length:', len(framework_html))
print('Done')
