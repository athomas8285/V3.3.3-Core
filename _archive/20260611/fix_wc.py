import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("D:/V3.3.3-Core/templates/index_new.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the accWC section in the HTML
idx = content.find("id=\"accWC\"")
if idx > 0:
    # Find the first acc-label after this
    label_idx = content.find("acc-label", idx)
    tag_end = content.find(">", label_idx) + 1
    tag_close = content.find("<", tag_end)
    print(f"Current label text: {repr(content[tag_end:tag_close])}")
    
    idx2 = content.find("id=\"accWC\"", idx + 1)
    print(f"Occurrences of id=accWC: {content.count('accWC')}")
    
# Check all Chinese text in sidebar area
acc_start = content.find("<div class=\"acc open\"")
acc_end = content.find("sd-wc-divider")
if acc_start > 0 and acc_end > 0:
    section = content[acc_start:acc_end]
    print(f"\nSidebar WC section ({len(section)} bytes):")
    print(section[:800])
