c = open('D:/V3.3.3-Core/templates/index.html','r',encoding='utf-8-sig').read()

# Find the exact position of the analysis section
idx1 = c.find('\u4eca\u65e5\u8d5b\u4e8b\u5206\u6790')
if idx1 > 0:
    # Go back to find the sec-header div
    start = c.rfind('<div', idx1-100, idx1)
    if start > 0:
        div_tag = c[start:idx1]
        if 'style=' not in div_tag:
            c = c[:start] + '<div class="sec-header" style="display:none">' + c[start+len('<div class="sec-header">'):]
            print('Analysis hidden at', start)
        else:
            print('Already has style')

idx2 = c.find('\u5f80\u65e5\u6570\u636e\u590d\u76d8')
if idx2 > 0:
    start2 = c.rfind('<div', idx2-100, idx2)
    if start2 > 0:
        div_tag2 = c[start2:idx2]
        if 'style=' not in div_tag2:
            c = c[:start2] + '<div class="sec-header" style="display:none;margin-top:20px">' + c[start2+len('<div class="sec-header" style="margin-top:20px">'):]
            print('Review hidden at', start2)
        else:
            print('Already has style')

open('D:/V3.3.3-Core/templates/index.html','w',encoding='utf-8').write(c)
print('Done')