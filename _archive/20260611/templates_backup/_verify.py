f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "r", encoding="utf-8")
c = f.read()
f.close()

# Check for mojibake
mojibake = c.count("\ufffd")
print(f"Replacement characters (U+FFFD): {mojibake}")

# Check key clean text
checks = [
    "V3.3.3-Core 是一套完整的足球比赛预测与分析框架",
    "核心球员缺阵对攻防能力的量化影响",
    "从竞彩SP反推市场隐含lambda",
    "DDI振幅比例参数化",
    "新增数据缺失标记系统",
    "凯利系数，控制资金管理模型的风险偏好",
    "常规联赛：战意修正上限+-15%",
    "margin:0 80px 0 40px",
    "共" + "' + total + " + "'场· 命中" + "'"
]
for check in checks:
    if check in c:
        print(f"  OK: {check[:50]}")
    else:
        print(f"  MISSING: {check[:50]}")

# Check overall structure
for tag in ["<!DOCTYPE html>", "<html", "<head>", "<title>", "</head>", "<body>", "</body>", "</html>"]:
    if tag in c:
        print(f"  Structure OK: {tag}")
    else:
        print(f"  MISSING: {tag}")

# Check spPanel sections
for section in ["V3.3.3-Core 分析框架", "框架参数说明", "分析系统介绍", "核心逻辑", "版本更新", "蒙特卡洛模拟", "风控降级", "战意修正"]:
    if section in c:
        print(f"  Section present: {section}")
    else:
        print(f"  Section MISSING: {section}")
