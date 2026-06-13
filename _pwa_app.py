content = open("D:/V3.3.3-Core/app.py","r",encoding="utf-8").read()
old = '''@app.route('/live.js')
def live_js():
    from flask import Response
    with open(os.path.join(BASE_DIR, 'templates', 'live.js'), 'r', encoding='utf-8') as f:
        return Response(f.read(), mimetype='application/javascript')'''
new = '''@app.route('/live.js')
def live_js():
    from flask import Response
    with open(os.path.join(BASE_DIR, 'templates', 'live.js'), 'r', encoding='utf-8') as f:
        return Response(f.read(), mimetype='application/javascript')

@app.route('/sw.js')
def sw_js():
    from flask import Response
    with open(os.path.join(BASE_DIR, 'static', 'sw.js'), 'r', encoding='utf-8') as f:
        return Response(f.read(), mimetype='application/javascript')'''
content = content.replace(old, new)
open("D:/V3.3.3-Core/app.py","w",encoding="utf-8").write(content)
print("OK")
