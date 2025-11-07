from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/qAbUy4XmZkKrV2jBc')
def dashboard():
    return send_from_directory(BASE_DIR, 'dashboard.html')

@app.route('/<path:filename>')
def serve_file(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.isfile(file_path):
        return send_from_directory(BASE_DIR, filename)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
