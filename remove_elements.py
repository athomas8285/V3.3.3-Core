import re

with open(r'D:\V3.3.3-Core\templates\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove trendArrow var declaration line
content = re.sub(r'var trendArrow=ld>=0\?["\u25b2\u25bc]+:["\u25b2\u25bc]+;\s*\n?', '', content)

# 2. Remove the trend span from the rating-score line
# Old: h+="<span class=\"trend\" style=\"color:"+(ld>=0?"#10b981":"#ef4444")+"\">"+trendArrow+"</span></div></div></div>";
# New: h+="</div></div></div>";
content = content.replace(
    '<span class=\\"trend\\" style=\\"color:"+(ld>=0?"#10b981":"#ef4444")+"\\">"+trendArrow+"</span>',
    ''
)

# 3. Remove the expand-arrow div line
content = re.sub(r'h\+\="<div class=\\"expand-arrow\\">.+</div>";\s*\n', '', content)

with open(r'D:\V3.3.3-Core\templates\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
