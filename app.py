from flask import Flask, send_from_directory
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/qA8uY4wXZk6rV2jBc')
def dashboard():
    return send_from_directory(BASE_DIR, 'dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
