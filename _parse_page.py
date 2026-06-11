import urllib.request
r = urllib.request.urlopen("https://web-production-d6f08.up.railway.app/", timeout=15)
d = r.read()
# Find rendered cards (not template JS code)
# Search for the JS template building cards - look for renderMatchCard
idx = d.find(b"renderMatchCard")
if idx > 0:
    # Find the actual function content
    print("renderMatchCard found at byte", idx)
    
# Search for grid-col-expand in template code (JS string)
# This will show us how the default card is built
idx2 = d.find(b"grid-col-expand")
if idx2 > 0:
    context = d[idx2-500:idx2+200]
    print("\n=== Card collapse row (near grid-col-expand) ===")
    print(context.decode("utf-8", errors="replace"))
