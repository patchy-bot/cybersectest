# web3/param/app.py
import os
import requests
from flask import Flask, request, abort, jsonify
from urllib.parse import urlparse

app = Flask(__name__)
BACKEND_URL = 'https://internal.example.com/transfer'

# Allowlist of target domains for SSRF protection
ALLOWED_DOMAINS = {'internal.example.com'}

def is_allowed_url(target: str) -> bool:
    try:
        parsed = urlparse(target)
        host = parsed.hostname
        return parsed.scheme in ('http', 'https') and host in ALLOWED_DOMAINS
    except Exception:
        return False

@app.route('/relay', methods=['POST'])
def relay_transfer():
    payload = request.get_json()
    if not payload or 'url' not in payload or 'data' not in payload:
        abort(400, 'Invalid payload')
    target = payload['url']
    if not is_allowed_url(target):
        abort(400, 'URL not permitted')
    # Forward the request safely
    try:
        resp = requests.post(target, json=payload['data'], timeout=5, allow_redirects=False)
    except requests.RequestException:
        abort(502, 'Bad gateway')
    return jsonify({'status': resp.status_code, 'response': resp.json()}), resp.status_code

if __name__ == '__main__':
    app.run(debug=False)