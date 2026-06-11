import sys

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 找到renderReview中 yr.forEach 的位置
rr_start = content.find("function renderReview(){")
yr_loop = content.find("yr.forEach(function(m){", rr_start)
print(f"yr.forEach 在位置: {yr_loop}")
if yr_loop >= 0:
    # 打印上下文
    print(f"上下文: {content[yr_loop-50:yr_loop+80]}")

# 也找到最后的 innerHTML 设置
rv_html = content.find("document.getElementById('rv').innerHTML=h;", rr_start)
print(f"rv.innerHTML 在位置: {rv_html}")
if rv_html >= 0:
    print(f"上下文: {content[rv_html-30:rv_html+60]}")

# 找到有预测数据的时候（从if(yr.length)到最后的else）
if_section = content.find("if(yr.length){", rr_start)
print(f"if(yr.length) 在位置: {if_section}")
str_len = 200
print(f"上下文: {content[if_section:if_section+str_len]}")