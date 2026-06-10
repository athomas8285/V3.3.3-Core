path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

line = lines[203]  # L204

# 从位置1230开始打印一段长内容
print("位置 1230-2500:")
section = line[1230:1550]
print(section)
print()
print("---")
print("位置 1550-1800:")
print(line[1550:1800])
print()
print("---")
print("位置 1800-2100:")
print(line[1800:2100])