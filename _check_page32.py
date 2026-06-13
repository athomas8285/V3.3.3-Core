with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# The block we need to modify: just before 'renderFromWC();' in the XHR callback
# We want to add merge logic after WC_MATCHES_DATA is built
old_end = '        renderFromWC();'

new_code = '''        // Merge rating results into WC_MATCHES_DATA
        if(typeof __DATA !== 'undefined' && __DATA && __DATA.rating){
          var ratingById = {};
          __DATA.rating.forEach(function(r){ if(r.id) ratingById[r.id]=r; });
          WC_MATCHES_DATA.forEach(function(wm){
            var r = ratingById[wm.id];
            if(r && r.actual_score){
              wm.result = r.actual_score;
              wm.half_full = r.half_full || '';
              wm.hit = r.hit === true;
              wm.dir = r.direction || wm.dir;
            }
          });
        }
        renderFromWC();'''

if new_code.count('        renderFromWC();') == 1:
    # Use the OLD one at the end
    pass

count_before = html.count(old_end)
print(f"'renderFromWC();' appears {count_before} times")

# Replace ONLY the one in the XHR callback (which is after the map())
# Find the specific occurrence
idx = html.rfind(old_end)  
# Actually there might be multiple - let's find the one inside the xhr.onload
xhr_start = html.find('xhr.onload = function')
xhr_end = html.find('xhr.onerror', xhr_start)
xhr_section = html[xhr_start:xhr_end]
rwc_in_xhr = xhr_section.rfind('renderFromWC();')
if rwc_in_xhr >= 0:
    abs_pos = xhr_start + rwc_in_xhr
    # Replace this specific occurrence
    html = html[:abs_pos] + new_code + html[abs_pos + len(old_end):]
    with open("D:\\V3.3.3-Core\\templates\\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Replaced at position {abs_pos}")
else:
    print("Not found in XHR callback!")