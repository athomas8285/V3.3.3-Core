with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the XHR callback that calls renderFromWC()
idx = html.find('WC_MATCHES_DATA = raw.map')
if idx >= 0:
    # Find the block - from WC_MATCHES_DATA assignment to renderFromWC() call
    block_end = html.find('renderFromWC()', idx)
    if block_end >= 0:
        block_end += len('renderFromWC()')
        block = html[idx:block_end]
        with open("_xhr_block.txt", "w", encoding="utf-8") as out:
            out.write(block)
        print(f"XHR block length: {len(block)}")
        print(f"Block starts at: {idx}")
        print(f"Block ends at: {block_end}")
        
        # Check if it ends with ';'
        if html[block_end:block_end+1] == ';':
            block_end += 1
        print(f"After block: {repr(html[block_end:block_end+20])}")