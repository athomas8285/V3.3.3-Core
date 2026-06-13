with open("D:\\V3.3.3-Core\\templates\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# The file has \\u6708 and \\u65e5 as literal escape sequences in JS code
# Python reads them as literal backslash-u characters
# So we search for the literal string
old_text = 'var isCollapsed = (dk === "6\\u670812\\u65e5");'
new_text = 'var allDoneWC = ml.every(function(m){ return !!m.result; });'

# Check if old_text exists
idx = html.find(old_text)
if idx >= 0:
    print(f"Found at {idx}")
    # Now find the surrounding context to replace the full block
    # The block includes the old_text line plus the following 5 lines
    block_start = idx
    block_end = html.find("h += '<div class=\"ana-date-body\"", idx)
    if block_end >= 0:
        block_end = html.find(">';", block_end) + 3
        print(f"Block from {block_start} to {block_end}")
        old_block = html[block_start:block_end]
        with open("_old_block.txt", "w", encoding="utf-8") as out:
            out.write(repr(old_block))
        
        new_block = '''    var allDoneWC = ml.every(function(m){ return !!m.result; });
    h += '<div class="ana-date-group">';
    h += '<div class="ana-date-label clickable" onclick="toggleDateGroup(this)">';
    h += '<span class="ana-date-arrow">' + (allDoneWC ? '\\u25b6' : '\\u25bc') + '</span> \\ud83d\\udcc5 ' + dk + '<span class="adl-count">' + ml.length + ' \\u573a</span></div>';
    h += '<div class="ana-date-body"' + (allDoneWC ? ' style="display:none"' : '') + '>';'''
        
        html = html[:block_start] + new_block + html[block_end:]
        with open("D:\\V3.3.3-Core\\templates\\index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Replaced!")
else:
    print("Not found as literal")
    # Check what the file actually has
    idx2 = html.find('var isCollapsed')
    if idx2 >= 0:
        ctx = html[idx2:idx2+80]
        with open("_ctx.txt", "w", encoding="utf-8") as out:
            out.write(repr(ctx))
        print("Context written")