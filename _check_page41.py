with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the broken code section
bad_code = '''                // Merge rating results into WC_MATCHES_DATA
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
        renderFromWC(); catch(e){ console.error("WC data parse error", e); }
    }
  };'''

good_code = '''                // Merge rating results into WC_MATCHES_DATA
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
        renderFromWC();
      } catch(e){ console.error("WC data parse error", e); }
    }
  };'''

count = html.count(bad_code)
print(f"Found bad code: {count}")

if count > 0:
    html = html.replace(bad_code, good_code)
    with open("D:\\V3.3.3-Core\\templates\\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Fixed!")
else:
    print("Pattern not found, checking...")
    idx = html.find('// Merge rating results')
    if idx >= 0:
        ctx = html[idx:idx+500]
        with open("_bad_ctx.txt", "w", encoding="utf-8") as out:
            out.write(ctx)
        print("Found merge code, context written")