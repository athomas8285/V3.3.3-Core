
c = open("D:/V3.3.3-Core/templates/index.html","r",encoding="utf-8-sig").read()
# Hide old analysis section
c = c.replace(
    '<div class="sec-header">\n    <h2>今日赛事分析</h2>',
    '<div class="sec-header" style="display:none">\n    <h2>今日赛事分析</h2>'
)
# Hide old review section  
c = c.replace(
    '<div class="sec-header" style="margin-top:20px">\n    <h2>往日数据复盘</h2>',
    '<div class="sec-header" style="display:none;margin-top:20px">\n    <h2>往日数据复盘</h2>'
)
open("D:/V3.3.3-Core/templates/index.html","w",encoding="utf-8").write(c)
print("Done")
