f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "r", encoding="utf-8")
c = f.read()
f.close()
lines = c.split("\n")
bad = [(i, l) for i, l in enumerate(lines) if "\ufffd" in l]
print(f"Found {len(bad)} lines with FFFD:")
for i, l in bad:
    # extract context around the FFFD
    idx = l.index("\ufffd")
    start = max(0, idx - 20)
    end = min(len(l), idx + 20)
    context = l[start:end].replace("\ufffd", "?")
    print(f"  Line {i}: ...{context}...")
