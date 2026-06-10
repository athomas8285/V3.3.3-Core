import sys
path = r'C:\Users\gjj\Desktop\v333\templates\charts.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# The search text in the file
old = q"q).join('') +'</div></div>' +'<span class="sec-l"></span></div>';q"
idx = content.find(old)
print('Found at offset:', idx)
if idx >= 0:
    event_html = (
        "+'<div style=\"border-top:1px solid var(--bd);margin:6px 0 4px;padding-top:6px\">'"
        "+'<div style=\"font-size:10px;color:var(--t3);font-weight:600;margin-bottom:4px;letter-spacing:0.3px\">" 
        "\u8d5b\u4e8b\u7c7b\u578b</div>'"
        "+'<label style=\"display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px\">"
        "<input type=\"checkbox\" '+(FILTER_ALL_EVENTS?'checked':'')+' onchange=\"setFilter(\\'event_all\\',\\'all\\')\" style=\"margin:0\">"
        "<span>\u5168\u90e8\u8d5b\u4e8b</span></label>'"
        "+_DATA.rating.reduce(function(acc,x){var ev=x.event||'';if(ev&&acc.indexOf(ev)<0)acc.push(ev);return acc;},[]).map(function(ev){"
        "return'<label style=\"display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px\">"
        "<input type=\"checkbox\" '+(FILTER_ALL_EVENTS||FILTER.event[ev]?'checked':'')+' onchange=\"setFilter(\\'event\\',\\''+ev+'\\')\" style=\"margin:0\">"
        "<span>'+ev+'</span></label>';}).join('')"
        "+'</div>'"
    )
    new_part = event_html + "+'</div></div>' +'<span class=\"sec-l\"></span></div>';"
    content = content[:idx] + new_part + content[idx+len(old):]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Replacement done!')
else:
    print('Pattern not found')