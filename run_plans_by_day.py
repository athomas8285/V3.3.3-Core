import json, os, sys, shutil

BASE = r"D:\V3.3.3-Core"
DATA = os.path.join(BASE, "data")
sys.path.insert(0, BASE)

from gen_plan import generate_plan
from gen_plan_html import build_html

prefixes = ["周四", "周五", "周六", "周日", "周一", "周二", "周三"]
day_labels = {"周四":"6/12","周五":"6/13","周六":"6/14","周日":"6/15","周一":"6/16","周二":"6/17","周三":"6/18"}
out_dir = r"C:\Users\gjj\Documents\Codex\2026-06-21\b-d-v3-3-3-core\outputs"

for prefix in prefixes:
    label = day_labels.get(prefix, prefix)
    print(f"\n=== {label} ({prefix}) ===")
    data = generate_plan(match_filter=prefix)

    if data["top"]:
        t = data["top"]
        print(f"  Top: {t['l1']['option']}@{t['l1']['odds']} x {t['l2']['option']}@{t['l2']['odds']} = {t['odds']}")
    print(f"  Legs: {data['total_legs']} | 2.0: {data['plan_2_count']} | 3.0: {data['plan_3_count']}")

    html = build_html(data)
    html_name = f"plan_{prefix}.html"
    json_name = f"plan_data_{prefix}.json"

    with open(os.path.join(DATA, html_name), "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy2(os.path.join(DATA, html_name), os.path.join(out_dir, html_name))
    shutil.copy2(os.path.join(DATA, "plan_data.json"), os.path.join(out_dir, json_name))
    print(f"  -> {html_name} + {json_name}")

print("\nDone!")
