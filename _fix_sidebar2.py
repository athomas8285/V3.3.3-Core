import sys
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()
changes = []

# 1. Remove old accToday CSS
old1 = "#accToday.open>.acc-head{background:linear-gradient(90deg,rgba(0,230,118,.06),transparent 60%)}"
old2 = "#accToday.open>.acc-head .acc-label{color:var(--green)}"
for old in [old1, old2]:
    if old in html:
        html = html.replace(old, "")
        changes.append("Removed old accToday CSS")

# 2. Add WC CSS
wc_css = """
/* WC sidebar */
#accWCMain .acc-head{border-radius:6px;margin:4px 8px}
#accWCMain.open>.acc-head .acc-label{color:var(--gold);text-shadow:0 0 12px rgba(251,191,36,.15)}
.wc-sub-item{display:flex;align-items:center;gap:10px;padding:9px 12px;margin:3px 8px;border-radius:6px;cursor:pointer;transition:all .15s;font-size:13px;color:var(--t2)}
.wc-sub-item:hover{background:rgba(251,191,36,.06);color:var(--t1)}
.wc-sub-item .wsi-icon{font-size:15px;flex-shrink:0}
.wc-sub-item .wsi-label{flex:1}
.sd-wc-badge{font-size:9px;color:var(--gold);background:rgba(251,191,36,.14);padding:1px 7px;border-radius:8px;letter-spacing:.3px;white-space:nowrap}
#accHistory,#accBacktest,#accDoc{opacity:.7;transition:opacity .2s}
#accHistory:hover,#accBacktest:hover,#accDoc:hover{opacity:1}
"""
marker = ".sd-wc-divider{height:1px;margin:8px 18px;background:linear-gradient(90deg,rgba(251,191,36,.12),transparent 60%)}"
if marker in html:
    html = html.replace(marker, marker + "\n" + wc_css.strip())
    changes.append("Added WC sidebar CSS")

# 3. Fix JS ref
if 'openAccordion("accToday")' in html:
    html = html.replace('openAccordion("accToday")', 'openAccordion("accWCMain")')
    changes.append("Fixed JS openAccordion ref")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Changes: {len(changes)}")
for c in changes:
    print(f"  - {c}")
