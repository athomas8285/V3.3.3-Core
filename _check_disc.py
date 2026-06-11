import urllib.request

r = urllib.request.urlopen('http://127.0.0.1:5020/', timeout=5)
html = r.read()
print('Size:', len(html))

if len(html) < 300000:
    content = html.decode('utf-8')
    
    # Check disclaimer
    disc_css = content.find('.ft-disclaimer')
    disc_html_full = content.find('ft-disclaimer')
    print('First ft-disclaimer at:', disc_html_full)
    
    # Check for the HTML tag
    tag_search = 'class=\"ft-disclaimer\"'
    tag_start = content.find(tag_search)
    print('HTML class=ft-disclaimer at:', tag_start)
    
    # Show context
    if tag_start >= 0:
        print('Context:', content[tag_start-60:tag_start+200])
    
    # Check before </body>
    body_pos = content.rfind('</body>')
    print()
    print('Last 200 chars before </body>:')
    print(content[body_pos-200:body_pos])
else:
    print('File TOO LARGE - corrupted')
