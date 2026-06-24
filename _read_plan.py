import json
with open("D:/V3.3.3-Core/data/plan_data.json", "r", encoding="utf-8", errors="replace") as f:
    pd = json.load(f)

print("=== 最推荐 ===")
t = pd.get("top")
if t:
    print(json.dumps(t, ensure_ascii=False, indent=2)[:600])
else:
    print("None")

print("\n=== 2.0方案 TOP5 ===")
for c in pd.get("plan_2", [])[:5]:
    print(json.dumps(c, ensure_ascii=False, indent=2)[:400])
    print("---")

print("\n=== 3.0方案 TOP5 ===")
for c in pd.get("plan_3", [])[:5]:
    print(json.dumps(c, ensure_ascii=False, indent=2)[:400])
    print("---")

print(f"\ntotal legs: {pd.get('total_legs')}")
print(f"2.0方案: {pd.get('plan_2_count')} 个")
print(f"3.0方案: {pd.get('plan_3_count')} 个")