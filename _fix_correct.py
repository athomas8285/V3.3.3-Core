f = open('D:/V3.3.3-Core/templates/index.html', 'r', encoding='utf-8')
c = f.read()
f.close()

script_pos = c.find('<script>', 68000)
print('Script at:', script_pos)

# Find the stray </div> (closest to script)
stray = c.rfind('</div>', 0, script_pos)
print('Stray (last) at:', stray)

# Find the main-close (one before stray)
main_close = c.rfind('</div>', 0, stray)
print('Main close at:', main_close)
print('Context around main close:', repr(c[main_close-30:main_close+30]))

# Insert disclaimer BEFORE main_close
disc = '''\\n<!-- \\u514d\\u8d23\\u58f0\\u660e -->
<div class="ft-disclaimer">
  <div class="ft-row">
    \\u26a0\\ufe0f \\u514d\\u8d23\\u58f0\\u660e\\uff1a\\u672c\\u7f51\\u7ad9\\u6240\\u63d0\\u4f9b\\u7684\\u6240\\u6709\\u8d5b\\u4e8b\\u5206\\u6790\\u53ca\\u9884\\u6d4b\\u7ed3\\u679c\\uff0c\\u4ec5\\u4f9b\\u4f53\\u80b2\\u7231\\u597d\\u8005\\u4ea4\\u6d41\\u53c2\\u8003\\uff0c\\u4e0d\\u6784\\u6210\\u4efb\\u4f55\\u6295\\u6ce8\\u5efa\\u8bae\\u6216\\u627f\\u8bfa\\u3002
  </div>
  <div class="ft-row">
    \\u26a0\\ufe0f \\u5f69\\u7968\\u6709\\u98ce\\u9669\\uff0c\\u6295\\u6ce8\\u9700\\u8c28\\u614e\\u3002\\u8bf7\\u7406\\u6027\\u8d2d\\u5f69\\uff0c\\u91cf\\u529b\\u800c\\u884c\\u3002\\u672a\\u6ee118\\u5c81\\u4e0d\\u5f97\\u8d2d\\u4e70\\u5f69\\u7968\\u3002
  </div>
</div>'''

c = c[:main_close] + disc + '\\n' + c[main_close:]

with open('D:/V3.3.3-Core/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Disclaimer inserted BEFORE .main close')
