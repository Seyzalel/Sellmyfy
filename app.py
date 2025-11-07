from flask import Flask, send_from_directory, abort, Response
import os, requests

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def root():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/qAbUy4XmZkKrV2jBc')
def dashboard_plain():
    return send_from_directory(BASE_DIR, 'dashboard.html')

@app.route('/notify', methods=['GET'])
def notify():
    try:
        r = requests.get('http://192.0.0.4:5000/notify', timeout=5)
        return (r.content, r.status_code, [('Content-Type', r.headers.get('Content-Type','application/octet-stream'))])
    except Exception:
        return ('', 204)

@app.route('/<path:filename>')
def any_file(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.isfile(path):
        return send_from_directory(BASE_DIR, filename)
    abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
