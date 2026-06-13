html_content = open('D:\\V3.3.3-Core\\templates\\index.html', 'r', encoding='utf-8').read()
script_start = html_content.index('<script>') + 8
script_end = html_content.index('</script>')
full_script = html_content[script_start:script_end]

opens = full_script.count('{')
closes = full_script.count('}')
print(f'Curly braces: {{ = {opens}, }} = {closes}, diff = {opens - closes}')

opens_b = full_script.count('[')
closes_b = full_script.count(']')
print(f'Brackets: [ = {opens_b}, ] = {closes_b}, diff = {opens_b - closes_b}')

opens_p = full_script.count('(')
closes_p = full_script.count(')')
print(f'Parentheses: ( = {opens_p}, ) = {closes_p}, diff = {opens_p - closes_p}')

backticks = full_script.count(chr(96))
print(f'Backticks: {backticks} (should be even)')

open_comments = full_script.count('/*')
close_comments = full_script.count('*/')
print(f'Block comments: /* = {open_comments}, */ = {close_comments}, diff = {open_comments - close_comments}')
