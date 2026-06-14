html_content = open('D:\\V3.3.3-Core\\templates\\index.html', 'r', encoding='utf-8').read()
script_start = html_content.index('<script>') + 8
script_end = html_content.index('</script>')
full_script = html_content[script_start:script_end]

# Find unclosed block comment
pos = full_script.find('/*')
while pos >= 0:
    close_pos = full_script.find('*/', pos + 2)
    if close_pos < 0:
        line_num = full_script[:pos].count('\n') + 1
        print(f'Unclosed /* at line ~{line_num}, char pos {pos}')
        print(f'Context: {repr(full_script[max(0,pos-50):pos+50])}')
    pos = full_script.find('/*', pos + 2)

# Find unclosed backtick (odd numbered)
count = 0
pos = -1
while True:
    pos = full_script.find(chr(96), pos + 1)
    if pos < 0:
        break
    count += 1
    if count == 13:  # Last one - unclosed
        line_num = full_script[:pos].count('\n') + 1
        print(f'\nUnclosed backtick at line ~{line_num}, char pos {pos}')
        print(f'Context before: {repr(full_script[max(0,pos-100):pos])}')
        print(f'Context after: {repr(full_script[pos:min(len(full_script),pos+100)])}')

# Track curly braces to find unclosed
depth = 0
for i, ch in enumerate(full_script):
    if ch == '{':
        depth += 1
    elif ch == '}':
        depth -= 1
    if depth < 0:
        print(f'\nExtra }} at pos {i}')
        depth = 0

print(f'\nFinal depth: {depth}')
if depth > 0:
    # Find last unclosed - scan backwards
    depth = 0
    unclosed_pos = -1
    for i in range(len(full_script) - 1, -1, -1):
        if full_script[i] == '}':
            depth += 1
        elif full_script[i] == '{':
            depth -= 1
            if depth < 0:
                unclosed_pos = i
                break
    if unclosed_pos >= 0:
        line_num = full_script[:unclosed_pos].count('\n') + 1
        print(f'Unclosed {{ at line ~{line_num}, char pos {unclosed_pos}')
        print(f'Context: {repr(full_script[max(0,unclosed_pos-100):unclosed_pos+50])}')
