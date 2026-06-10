import re

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the dropdown HTML
idx = content.find('filterDropdown')
# Search backward from that position for 'id=\"filterDropdown\"'
search_start = max(0, idx - 1000)
start_marker = 'id="filterDropdown"'
start = content.rfind(start_marker, search_start, idx)
print(f"Dropdown start at: {start}")
if start < 0:
    # Try with escaped quotes
    start_marker2 = 'id=\\"filterDropdown\\"'
    start = content.rfind(start_marker2, search_start, idx)
    print(f"Dropdown start (escaped) at: {start}")

# Find the end marker for the section
end_marker = "sec-l\"></span></div>';"
end = content.find(end_marker, start)
print(f"End marker at: {end}")
if end >= 0:
    end += len(end_marker)

if start >= 0 and end >= 0:
    old_section = content[start:end]
    print(f"Old section length: {len(old_section)}")
    
    # Find the rating checkboxes end - "}).join('')"
    join_end = old_section.rfind("}).join('')")
    print(f"join_end at: {join_end} in old_section")
    
    if join_end >= 0:
        before = old_section[:join_end]
        after = old_section[join_end:]
        
        event_section = (
            " +'<div style=\"border-top:1px solid var(--bd);margin:6px 0 4px;padding-top:6px\">"
            "+'<div style=\"font-size:10px;color:var(--t3);font-weight:600;margin-bottom:4px;letter-spacing:0.3px\">"
            + chr(36154) + chr(20107) + chr(31867) + chr(22411) + "</div>'"
            "+'<label style=\"display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px\">"
            "<input type=\"checkbox\" '+(FILTER_ALL_EVENTS?'checked':'')+' onchange=\"setFilter(\\'event_all\\',\\'all\\')\" style=\"margin:0\">"
            "<span>" + chr(20840) + chr(37096) + chr(36154) + chr(20107) + "</span></label>'"
            "+_DATA.rating.reduce(function(acc,x){var ev=x.event||'';if(ev&&acc.indexOf(ev)<0)acc.push(ev);return acc;},[]).map(function(ev){"
            "return'<label style=\"display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px\">"
            "<input type=\"checkbox\" '+(FILTER_ALL_EVENTS||FILTER.event[ev]?'checked':'')+' onchange=\"setFilter(\\'event\\',\\''+ev+'\\')\" style=\"margin:0\">"
            "<span>'+ev+'</span></label>';}).join('')"
            "+'</div>'"
        )
        
        new_after = after
        new_section = before + event_section + new_after
        content = content[:start] + new_section + content[end:]
        print("Replacement done!")
    else:
        print("join_end not found")
else:
    print(f"Cannot find: start={start}, end={end}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("File saved")