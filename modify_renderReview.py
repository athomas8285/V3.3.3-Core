import sys

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 找到renderReview函数
rr_start = content.find("function renderReview(){")
print(f"renderReview 起始: {rr_start}")

# 找到函数的h变量构建部分 - "var h='<div class=\"sec\">"（昨日复盘标题）
title_marker = "var h='<div class=\"sec\"><span class=\"sec-dot\"></span><span class=\"sec-h\">\u6628\u65e5\u626b\u76d8</span><span class=\"sec-l\"></span></div>';"
idx = content.find(title_marker, rr_start)
print(f"标题行: {idx}")

if idx >= 0:
    # 在这行之后插入筛选下拉菜单
    # 原来的行: var h='<div...>昨日扫盘</div>';
    # 改成: var h='<div...>昨日扫盘</div>' + dropdown_html;
    new_header = (
        "var h='<div class=\"sec\"><span class=\"sec-dot\"></span><span class=\"sec-h\">\u6628\u65e5\u626b\u76d8</span>'"
        "+'<div style=\"position:relative;margin-left:8px;display:inline-block\">'"
        "+'<span onclick=\"toggleFilterRV()\" style=\"cursor:pointer;background:var(--surface-2);border:1px solid var(--bd);border-radius:4px;padding:2px 8px;font-size:11px;color:var(--t2);font-family:var(--sans);white-space:nowrap;user-select:none\">\u7b5b\u9009 \u25bc</span>'"
        "+'<div id=\"filterDropdownRV\" style=\"display:none;position:absolute;top:100%;left:0;margin-top:4px;background:var(--surface);border:1px solid var(--bd);border-radius:6px;padding:8px;z-index:50;min-width:160px;box-shadow:0 4px 12px rgba(0,0,0,0.1)\">'"
        "+'<div style=\"font-size:10px;color:var(--t3);font-weight:600;margin-bottom:4px;letter-spacing:0.3px\">\u63a8\u8350\u7b49\u7ea7</div>'"
        "+['S','A','B','C'].map(function(l){return'<label style=\"display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px\"><input type=\"checkbox\" '+(FILTER_RV.rating[l]?'checked':'')+' onchange=\"setFilterRV(\\'rating\\',\\''+l+'\\')\" style=\"margin:0\"><span>'+l+'\u7ea7</span></label>';}).join('')"
        "+'<div style=\"border-top:1px solid var(--bd);margin:6px 0 4px;padding-top:6px\">'"
        "+'<div style=\"font-size:10px;color:var(--t3);font-weight:600;margin-bottom:4px;letter-spacing:0.3px\">\u8d5b\u4e8b\u7c7b\u578b</div>'"
        "+'<label style=\"display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px\"><input type=\"checkbox\" '+(FILTER_RV_ALL_EVENTS?'checked':'')+' onchange=\"setFilterRV(\\'event_all\\',\\'all\\')\" style=\"margin:0\"><span>\u5168\u90e8\u8d5b\u4e8b</span></label>'"
        "+RV.reduce(function(acc,x){var ev=x.event||'';if(ev&&acc.indexOf(ev)<0)acc.push(ev);return acc;},[]).map(function(ev){return'<label style=\"display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px\"><input type=\"checkbox\" '+(FILTER_RV_ALL_EVENTS||FILTER_RV.event[ev]?'checked':'')+' onchange=\"setFilterRV(\\'event\\',\\''+ev+'\\')\" style=\"margin:0\"><span>'+ev+'</span></label>';}).join('')"
        "+'</div>'"
        "+'<div style=\"border-top:1px solid var(--bd);margin:6px 0 4px;padding-top:6px\">'"
        "+'<div style=\"font-size:10px;color:var(--t3);font-weight:600;margin-bottom:4px;letter-spacing:0.3px\">\u6b63\u786e\u7edf\u8ba1</div>'"
        "+['\u65b9\u5411','\u603b\u8fdb\u7403','\u534a\u5168\u573a','\u6bd4\u5206'].map(function(k){"
        "var v={'\u65b9\u5411':'dir','\u603b\u8fdb\u7403':'goals','\u534a\u5168\u573a':'ht','\u6bd4\u5206':'score'}[k];"
        "return'<label style=\"display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px\">'"
        "+'<input type=\"checkbox\" '+(FILTER_RV[v]?'checked':'')+' onchange=\"setFilterRV(\\'correct\\',\\''+v+'\\')\" style=\"margin:0\">'"
        "+'<span>'+k+'\u6b63\u786e</span></label>';}).join('')"
        "+'</div></div></div>'"
        "+'<span class=\"sec-l\"></span></div>';"
    )
    
    content = content.replace(title_marker, new_header)
    print("标题行替换完成!")
else:
    print("标题行未找到!")
    # 搜索更广泛的模式
    alt = "昨日扫盘"
    idx2 = content.find(alt, rr_start)
    if idx2 >= 0:
        print(f"'昨日扫盘' 在位置 {idx2}")
        print(repr(content[idx2-30:idx2+100]))

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("保存成功!")