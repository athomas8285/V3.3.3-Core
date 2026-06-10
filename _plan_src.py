import json, math
from datetime import datetime

def poisson_pmf(k, lam):
    if lam <= 0:
        return 0.0
    return (lam ** k) * math.exp(-lam) / math.factorial(k)

def load_today_data():
    base = "D:\\V3.3.3-Core\\data"
    with open(base + "\\match_info.json", "r", encoding="utf-8") as f:
        info = json.load(f)["matches"]
    with open(base + "\\monte_carlo_result.json", "r", encoding="utf-8") as f:
        mc = json.load(f)["matches"]
    with open(base + "\\rating_result.json", "r", encoding="utf-8") as f:
        rating = json.load(f)["matches"]
    info_map = {m["id"]: m for m in info}
    mc_map = {m["id"]: m for m in mc}
    rating_map = {m["id"]: m for m in rating}
    return info_map, mc_map, rating_map

print("test")