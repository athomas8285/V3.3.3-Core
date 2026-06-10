with open("index.html","r",encoding="utf-8") as f:
    t = f.read()

# First sp-g-tl: add expanded + open
t = t.replace(
    '<div class="sp-g sp-g-tl">',
    '<div class="sp-g sp-g-tl expanded">',
    1
)
t = t.replace(
    'V3.3.3-Core 分析框架</div>\n    <div class="sp-g-c">',
    'V3.3.3-Core 分析框架</div>\n    <div class="sp-g-c open">',
    1
)

# Second sp-g-tl: Find it and add expanded + open
# Find the second occurrence
idx = t.index('<div class="sp-g sp-g-tl">')
t = t[:idx] + t[idx:].replace(
    '<div class="sp-g sp-g-tl">',
    '<div class="sp-g sp-g-tl expanded">',
    1
)
idx2 = t.index('框架参数说明</div>\n    <div class="sp-g-c">', idx)
t = t[:idx2] + t[idx2:].replace(
    '框架参数说明</div>\n    <div class="sp-g-c">',
    '框架参数说明</div>\n    <div class="sp-g-c open">',
    1
)

with open("index.html","w",encoding="utf-8") as f:
    f.write(t)
print("Done")