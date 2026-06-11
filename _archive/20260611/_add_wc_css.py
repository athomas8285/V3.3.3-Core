import sys
sys.stdout.reconfigure(encoding="utf-8")
path = "D:\\V3.3.3-Core\\templates\\index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

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
# Insert before the first .sd-divider in CSS (if found) or at end of CSS block
if ".sd-wc-divider" in html:
    html = html.replace(".sd-wc-divider", wc_css.strip() + "\n\n.sd-wc-divider")
    print("Inserted via sd-wc-divider")
elif '#accToday.open>.acc-head .acc-icon{color:var(--green)}' in html:
    html = html.replace('#accToday.open>.acc-head .acc-icon{color:var(--green)}', wc_css.strip() + "\n\n" + '#accToday.open>.acc-head .acc-icon{color:var(--green)}')
    print("Inserted after accToday icon CSS")
else:
    # Insert before </style> or end of CSS
    needle = ".sd-footer{padding:10px 16px;font-size:9px"
    if needle in html:
        html = html.replace(needle, wc_css.strip() + "\n\n" + needle)
        print("Inserted before sd-footer CSS")
    else:
        print("WARN: no insertion point found")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
