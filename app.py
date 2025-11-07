from flask import Flask, send_from_directory, request, abort, Response
import os, requests, concurrent.futures

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_BASE = os.getenv("TARGET_API", "http://192.0.0.4:5000")
_session = requests.Session()
_session.headers.update({"Connection": "keep-alive"})
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)

@app.route("/")
def root():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory(BASE_DIR, "dashboard.html")

@app.route("/notify", methods=["GET"])
def notify_async():
    url = API_BASE.rstrip("/") + "/notify"
    _executor.submit(_session.get, url, timeout=3)
    return Response(status=204)

@app.route("/notify-sync", methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"])
def notify_sync():
    url = API_BASE.rstrip("/") + "/notify"
    params = request.args.to_dict(flat=True)
    data = request.get_data()
    headers = {k: v for k, v in request.headers.items() if k.lower() not in {"host","content-length","accept-encoding","connection"}}
    try:
        r = _session.request(request.method, url, params=params, data=data, headers=headers, timeout=8)
        h = [(k, v) for k, v in r.headers.items() if k.lower() not in {"content-encoding","transfer-encoding","connection"}]
        return Response(response=r.content, status=r.status_code, headers=h)
    except requests.RequestException:
        return Response(status=502)

@app.route("/notify-beacon", methods=["POST"])
def notify_beacon():
    url = API_BASE.rstrip("/") + "/notify"
    _executor.submit(_session.get, url, timeout=3)
    return Response(status=204)

@app.route("/favicon.ico")
def favicon():
    path = os.path.join(BASE_DIR, "favicon.ico")
    if os.path.isfile(path):
        return send_from_directory(BASE_DIR, "favicon.ico")
    return Response(status=204)

@app.route("/<path:filename>")
def any_file(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.isfile(path):
        return send_from_directory(BASE_DIR, filename)
    abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)
