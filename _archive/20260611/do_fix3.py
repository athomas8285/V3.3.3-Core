import sys

path = r"C:\Users\gjj\Desktop\v333\templates\charts.js"

with open(path, "rb") as f:
    data = f.read()

# Search for the pattern
old_bytes = b"}).join('') +'</div></div>' +'<span class=\"sec-l\"></span></div>';"
idx = data.find(old_bytes)
print("Pattern found at byte:", idx)

if idx >= 0:
    # Build the new event type section (as bytes)
    event_part = (
        b"+'<div style=\"border-top:1px solid var(--bd);margin:6px 0 4px;padding-top:6px\">'"
        b"+'<div style=\"font-size:10px;color:var(--t3);font-weight:600;margin-bottom:4px;letter-spacing:0.3px\">"
        + chr(0x8d5b).encode('utf-8') + chr(0x4e8b).encode('utf-8') + chr(0x7c7b).encode('utf-8') + chr(0x578b).encode('utf-8')
        + b"</div>'"
        b"+'<label style=\"display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px\">"
        b"<input type=\"checkbox\" '+(FILTER_ALL_EVENTS?'checked':'')+' onchange=\"setFilter('event_all','all')\" style=\"margin:0\">"
        b"<span>"
        + chr(0x5168).encode('utf-8') + chr(0x90e8).encode('utf-8') + chr(0x8d5b).encode('utf-8') + chr(0x4e8b).encode('utf-8')
        + b"</span></label>'"
        b"+_DATA.rating.reduce(function(acc,x){var ev=x.event||'';if(ev&&acc.indexOf(ev)<0)acc.push(ev);return acc;},[]).map(function(ev){"
        b"return'<label style=\"display:flex;align-items:center;gap:6px;padding:3px 4px;cursor:pointer;font-size:12px;color:var(--t2);border-radius:3px\">"
        b"<input type=\"checkbox\" '+(FILTER_ALL_EVENTS||FILTER.event[ev]?'checked':'')+' onchange=\"setFilter('event','\"+ev+\"')\" style=\"margin:0\">"
        b"<span>'+ev+'</span></label>';}).join('')"
        b"+'</div>'"
    )
    
    new_bytes = event_part + b"+'</div></div>' +'<span class=\"sec-l\"></span></div>';"
    
    data = data[:idx] + new_bytes + data[idx+len(old_bytes):]
    
    with open(path, "wb") as f:
        f.write(data)
    print("File updated successfully!")
else:
    print("Pattern not found, trying alternative...")
    # Let's show what's around the area
    for search_start in range(len(data) - 100):
        chunk = data[search_start:search_start+50]
        if b"join" in chunk and b"sec-l" in chunk:
            print(f"Found some match at {search_start}: {chunk}")
            break