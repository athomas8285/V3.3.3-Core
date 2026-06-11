import re

f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "rb")
c = f.read()
f.close()

print("EFBFBD3F count:", c.count(b"\xef\xbf\xbd\x3f"))

fixes = [
    # 查询: 查 + (FFFD?) -> 查询
    (b"\xe6\x9f\xa5\xef\xbf\xbd\x3f", b"\xe6\x9f\xa5\xe8\xaf\xa2"),
    # ↑ 倒序: FFFD? -> ↑  
    (b">\xef\xbf\xbd\x3f\xe5\x80\x92\xe5\xba\x8f", b">\xe2\x86\x91 \xe5\x80\x92\xe5\xba\x8f"),
    # 加载中: 加载 + FFFD? -> 加载中
    (b"\xe5\x8a\xa0\xe8\xbd\xbd\xef\xbf\xbd\x3f", b"\xe5\x8a\xa0\xe8\xbd\xbd\xe4\xb8\xad"),
    # 扫盘数据: FFFD?FFFD?数据 -> 扫盘数据
    (b"\xef\xbf\xbd\x3f\xef\xbf\xbd\x3f\xe6\x95\xb0\xe6\x8d\xae", b"\xe6\x89\xab\xe7\x9b\x98\xe6\x95\xb0\xe6\x8d\xae"),
    # <em>扫盘</em>: <em>FFFD?FFFD?</em> -> <em>扫盘</em>
    (b"<em>\xef\xbf\xbd\x3f\xef\xbf\xbd\x3f</em>", b"<em>\xe6\x89\xab\xe7\x9b\x98</em>"),
    # ↓ 顺序 / ↑ 倒序 (JS)
    (b'SORT_ASC ? "\xef\xbf\xbd\x3f\xe9\xa1\xba\xe5\xba\x8f" : "\xef\xbf\xbd\x3f\xe5\x80\x92\xe5\xba\x8f"',
     b'SORT_ASC ? "\xe2\x86\x93 \xe9\xa1\xba\xe5\xba\x8f" : "\xe2\x86\x91 \xe5\x80\x92\xe5\xba\x8f"'),
    # 中 + 场 + · - the 场 after 命中
    (b"\xe4\xb8\xad\xef\xbf\xbd\x3f\xc2\xb7", b"\xe4\xb8\xad\xe5\x9c\xba\xc2\xb7"),
    # 共' + total + '场· 命中' - replace the whole expression
    (b"'\xef\xbf\xbd\x3f\xc2\xb7 ' +", b"' + total + '\xe5\x9c\xba\xc2\xb7 \xe5\x91\xbd\xe4\xb8\xad' +"),
    # 开始时间: 胜平FFFD? -> 胜平间 
    (b"\xe8\x83\x9c\xe5\xb9\xb3\xef\xbf\xbd\x3f", b"\xe8\x83\x9c\xe5\xb9\xb3\xe9\x97\xb4"),
    # ht !== '—' (em dash)
    (b"!== '\xef\xbf\xbd\x3f ? '/", b"!== '\xe2\x80\x94' ? '/"),
    # // Expanded — prediction
    (b"nded \xef\xbf\xbd\x3fpredic", b"nded \xe2\x80\x94 predic"),
]

count = 0
for old, new in fixes:
    if old in c:
        c = c.replace(old, new)
        print(f"Fixed ({count}): len={len(old)}")
        count += 1
    else:
        print(f"NOT FOUND ({count})")

remaining = c.count(b"\xef\xbf\xbd\x3f")
print(f"Remaining EFBFBD3F: {remaining}")
# Also check for lone FFFD
lone_fffd = len(re.findall(b"\xef\xbf\xbd", c))
print(f"Total FFFD byte sequences: {lone_fffd}")

f = open("C:/Users/gjj/Desktop/v333/templates/index.html", "wb")
f.write(c)
f.close()
print("DONE")
