f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "rb")
c = f.read()
f.close()

# Find the corrupted line
# Pattern: the line with disp + " 比赛预测</div>>"
pattern = b"h += '" + b"<div style=\"font-size:14px;font-weight:600;color:var(--ink)\">" + b"' + disp + ' "
idx = c.find(pattern)
if idx >= 0:
    line_start = c.rfind(b"\n", 0, idx)
    line_end = c.find(b"\n", idx)
    
    # Print what we found
    print(f"Found corrupted line at {idx}")
    print(f"Line range: {line_start} to {line_end}")
    
    # The correct two lines should be:
    line1 = b"    h += '<div style=\"font-size:14px;font-weight:600;color:var(--ink)\">' + disp + ' \xe6\xaf\x94\xe8\xb5\x9b\xe9\xa2\x84\xe6\xb5\x8b</div>';"
    line2 = b"    h += '<div style=\"font-size:11px;color:var(--t3);margin-top:4px\">\xe5\x85\xb1' + total + '\xe5\x9c\xba\xc2\xb7 \xe5\x91\xbd\xe4\xb8\xad' + hits + '\xe5\x9c\xba\xc2\xb7 ' + rate + '%</div>';"
    
    replacement = line1 + b"\r\n" + line2
    new_c = c[:line_start] + b"\n" + replacement + c[line_end:]
    
    print(f"Old line len: {line_end - line_start}")
    print(f"New lines len: {len(replacement)}")
    
    f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "wb")
    f.write(new_c)
    f.close()
    print("Done!")
else:
    print("Pattern not found!")
    # Try a broader search
    pattern2 = b"\xe6\xaf\x94\xe8\xb5\x9b\xe9\xa2\x84\xe6\xb5\x8b</div>>' + total +"
    idx2 = c.find(pattern2)
    if idx2 >= 0:
        print(f"Found alt pattern at {idx2}")
        line_start2 = c.rfind(b"\n", 0, idx2)
        line_end2 = c.find(b"\n", idx2)
        print(f"Line: {c[line_start2:line_end2]}")
