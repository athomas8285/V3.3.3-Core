import re

html_content = open('D:\\V3.3.3-Core\\templates\\index.html', 'r', encoding='utf-8').read()
script_start = html_content.index('<script>') + 8
script_end = html_content.index('</script>')
full_script = html_content[script_start:script_end]

i = 0
depth = 0
stack = []
escaped = False
in_string = None
in_regex = False

line_num = 1
while i < len(full_script):
    ch = full_script[i]
    
    if ch == '\n':
        line_num += 1
    
    if escaped:
        escaped = False
        i += 1
        continue
    
    if ch == '\\' and in_string:
        escaped = True
        i += 1
        continue
    
    if in_string:
        if ch == in_string:
            in_string = None
        i += 1
        continue
    
    if in_regex:
        if ch == '/' and not escaped:
            in_regex = False
        i += 1
        continue
    
    if ch in ("'", '"'):
        in_string = ch
        i += 1
        continue
    
    if ch == '/' and i + 1 < len(full_script):
        nxt = full_script[i+1]
        if nxt == '/':
            while i < len(full_script) and full_script[i] != '\n':
                i += 1
            continue
        elif nxt == '*':
            i += 2
            while i < len(full_script):
                if full_script[i] == '*' and i + 1 < len(full_script) and full_script[i+1] == '/':
                    i += 2
                    break
                if full_script[i] == '\n':
                    line_num += 1
                i += 1
            continue
        else:
            # Potential regex start
            prev = full_script[i-1] if i > 0 else ' '
            if prev in (' ', '=', ',', '(', '[', '!', '&', '|', '~', ':', ';', '{', '?'):
                in_regex = True
                i += 1
                continue
    
    if ch == '{':
        depth += 1
        stack.append((depth, i, line_num))
    elif ch == '}':
        depth -= 1
        if stack:
            stack.pop()
    
    i += 1

print(f'Final depth: {depth}')
if stack:
    print(f'Unclosed braces remaining: {len(stack)}')
    for d, pos, ln in stack:
        ctx = full_script[max(0,pos-80):pos+30]
        print(f'  Line ~{ln}, pos {pos}: ...{ctx}...')
