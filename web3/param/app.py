# web3/param/app.py
from flask import Flask, request, jsonify, abort
import requests
import os

app = Flask(__name__)
API_GATEWAY = os.getenv('PHP_GATEWAY_URL', 'http://localhost/gateway.php')
API_KEY = os.getenv('API_KEY')  # shared secret

@app.route('/transfer', methods=['POST'])
def transfer():
    # Authenticate request
    token = request.headers.get('X-API-KEY')
    if token != API_KEY:
        abort(401, description='Unauthorized')

    data = request.get_json()
    # Input validation
    from_acc = data.get('from')
    to_acc = data.get('to')
    amount = data.get('amount')
    if not isinstance(from_acc, str) or not isinstance(to_acc, str):
        abort(400, 'Account IDs must be strings')
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError()
    except:
        abort(400, 'Invalid amount')

    # Forward sanitized request to PHP gateway
    resp = requests.post(API_GATEWAY, json={
        'from': from_acc,
        'to': to_acc,
        'amount': amount
    }, timeout=5)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run()