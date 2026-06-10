import os, json
from flask import Flask, jsonify, Response

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

@app.route('/')
def index():
    with open(os.path.join(BASE_DIR, 'templates', 'index.html'), encoding='utf-8') as f:
        return f.read()

@app.route('/api/latest')
def get_latest():
    try:
        return jsonify({
            "rating": json.load(open(os.path.join(DATA_DIR, 'rating_result.json'), encoding='utf-8'))['matches'],
            "mc": json.load(open(os.path.join(DATA_DIR, 'monte_carlo_result.json'), encoding='utf-8'))['matches'],
            "info": json.load(open(os.path.join(DATA_DIR, 'match_info.json'), encoding='utf-8'))['matches'],
            "ddi": json.load(open(os.path.join(DATA_DIR, 'ddi_result.json'), encoding='utf-8'))['matches'],
            "ai": json.load(open(os.path.join(DATA_DIR, 'ai_judgment.json'), encoding='utf-8'))['matches']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/charts.js')
def charts_js():
    with open(os.path.join(BASE_DIR, 'templates', 'charts.js'), encoding='utf-8') as f:
        return Response(f.read(), mimetype='application/javascript')

@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
