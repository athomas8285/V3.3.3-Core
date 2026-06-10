path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_marker = r"sec-l"></span></div>';"
idx = content.find(old_marker)
print(f"sec-l marker at: {idx}")

# Go back to find the beginning of this section
sec_start = content.rfind("+'</div></div>' +'<span class=\"sec-l\"></span></div>';", 0, idx)
print(f"Section start at: {sec_start}")
if sec_start >= 0:
    old_section = content[sec_start:idx+len(old_marker)]
    print(f"Old section ({len(old_section)} chars): {repr(old_section)}")
    
    # Build the event type section to insert
    # It goes AFTER the rating checkboxes, BEFORE the </div></div> closing
    # We want: old_section was "plus + closing_divs"
    # We want new: "plus + event_html + closing_divs"
    # So we replace the entire old_section
    
    event_html = (
        "+'<div style=\"border-top:1px solid var(--bd);margin:6px 0 4px;padding-top:6px\">'"
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
    
    old_full = content[sec_start:idx+len(old_marker)]
    new_full = event_html + "+'</div></div>' +'<span class=\"sec-l\"></span></div>';"
    
    content = content[:sec_start] + new_full + content[idx+len(old_marker):]
    print("Replacement done!")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("File saved")
else:
    print("Section not found")