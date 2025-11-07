from flask import Flask, send_from_directory, abort, Response
import os
import uuid
import json
import requests
from datetime import datetime, timezone

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

API_TOKEN = "q98u7wX2ei23yN7B1hjq1dboEXpWSsGsNV8j"

def enviar_venda_utmify():
    url = "https://api.utmify.com.br/api-credentials/orders"
    headers = {
        "x-api-token": API_TOKEN,
        "Content-Type": "application/json"
    }
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
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code

@app.route("/")
def root():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory(BASE_DIR, "dashboard.html")

@app.route("/notify", methods=["GET"])
def notify():
    status = enviar_venda_utmify()
    return Response(status=status)

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
    app.run(host="0.0.0.0", port=8080)
