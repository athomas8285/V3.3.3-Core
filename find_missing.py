path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

line = lines[203]  # L204

# 搜索 1232 到 1400 之间的所有 } 字符
section = line[1232:1400]
for i, c in enumerate(section):
    if c == "}":
        global_pos = 1232 + i
        print(f"位置{global_pos}: }} -> 上下文: ...{line[max(0,global_pos-5):global_pos+5]}...")

print()
print("同理搜索所有 ) 字符:")
for i, c in enumerate(section):
    if c == ")":
        global_pos = 1232 + i
        print(f"位置{global_pos}: ) -> 上下文: ...{line[max(0,global_pos-5):global_pos+5]}...")