from flask import Flask, send_from_directory, request, Response, abort
import os
import uuid
import requests
import mimetypes
from datetime import datetime, timezone

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

API_TOKEN = "q98u7wX2ei23yN7B1hjq1dboEXpWSsGsNV8j"

def enviar_venda_utmify():
    url = "https://api.utmify.com.br/api-credentials/orders"
    headers = {"x-api-token": API_TOKEN, "Content-Type": "application/json"}
    now_utc = datetime.now(timezone.utc)
    created_at = now_utc.strftime("%Y-%m-%d %H:%M:%S")
    order_id = str(uuid.uuid4())
    payload = {
        "orderId": order_id,
        "platform": "PythonScript",
        "paymentMethod": "pix",
        "status": "paid",
        "createdAt": created_at,
        "approvedDate": created_at,
        "refundedAt": None,
        "customer": {
            "name": "Nome do Cliente",
            "email": "cliente@exemplo.com",
            "phone": "5511999999999",
            "document": "12345678901",
            "country": "US",
            "ip": "187.22.101.10"
        },
        "products": [
            {
                "id": "PROD-001",
                "name": "Infra-UCA",
                "planId": None,
                "planName": None,
                "quantity": 1,
                "priceInCents": 9981
            }
        ],
        "trackingParameters": {
            "src": None,
            "sck": None,
            "utm_source": None,
            "utm_campaign": None,
            "utm_medium": None,
            "utm_content": None,
            "utm_term": None
        },
        "commission": {
            "totalPriceInCents": 9981,
            "gatewayFeeInCents": 0,
            "userCommissionInCents": 9181,
            "currency": "BRL"
        },
        "isTest": False
    }
    r = requests.post(url, headers=headers, json=payload, timeout=10)
    return r.status_code

@app.after_request
def no_cache(r):
    p = request.path.lower()
    if p.endswith((".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".ico", ".svg", ".mp4", ".webm", ".ogv")) or p in ("/", "/dashboard"):
        r.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0, s-maxage=0, private"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers["Surrogate-Control"] = "no-store"
        r.headers["Vary"] = "*"
        r.headers.pop("ETag", None)
        r.headers.pop("Last-Modified", None)
    return r

def stream_range(path, mime):
    size = os.path.getsize(path)
    start = 0
    end = size - 1
    rng = request.headers.get("Range")
    if rng and rng.startswith("bytes="):
        s = rng.replace("bytes=", "").split("-", 1)
        if s[0].strip() != "":
            start = int(s[0])
        if len(s) > 1 and s[1].strip() != "":
            end = int(s[1])
        if end >= size:
            end = size - 1
        length = end - start + 1
        with open(path, "rb") as f:
            f.seek(start)
            data = f.read(length)
        res = Response(data, 206, mimetype=mime, direct_passthrough=True)
        res.headers["Content-Range"] = f"bytes {start}-{end}/{size}"
        res.headers["Accept-Ranges"] = "bytes"
        res.headers["Content-Length"] = str(length)
        return res
    with open(path, "rb") as f:
        data = f.read()
    res = Response(data, 200, mimetype=mime, direct_passthrough=True)
    res.headers["Content-Length"] = str(size)
    res.headers["Accept-Ranges"] = "bytes"
    return res

@app.route("/")
def root():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory(BASE_DIR, "dashboard.html")

@app.route("/notify", methods=["GET"])
def notify():
    status = enviar_venda_utmify()
    body = f'{{"upstream_status": {status}}}'
    return Response(body, status=200, mimetype="application/json")

@app.route("/media/<path:filename>")
def media(filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(path):
        abort(404)
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return stream_range(path, mime)

@app.route("/<path:filename>")
def any_file(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.isfile(path):
        ext = os.path.splitext(filename)[1].lower()
        if ext in (".mp4", ".webm", ".ogv"):
            mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
            return stream_range(path, mime)
        return send_from_directory(BASE_DIR, filename)
    abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)
