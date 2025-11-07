from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/qA8uY4wXZk6rV2jBc')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'dashboard.html')

if __name__ == '__main__':
    app.run()
