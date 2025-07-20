from flask import Flask, request, session, redirect, url_for, jsonify, abort
from functools import wraps
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'replace-with-secure-key')

# In-memory user store for demo; replace with real database
USERS = {
    'alice': {'password': 'alicepw', 'account': 'AliceAcc'},
    'bob':   {'password': 'bobpw',   'account': 'BobAcc'},
}

# Simple login_required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            abort(401, 'Authentication required')
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = USERS.get(username)
    if user and user['password'] == password:
        session['username'] = username
        session['account'] = user['account']
        return jsonify({'message': 'Logged in'})
    abort(401, 'Invalid credentials')

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    to_account = request.form.get('to_account', '').strip()
    amount_str = request.form.get('amount', '0').strip()

    # Input validation
    if not to_account or to_account == session['account']:
        abort(400, 'Invalid target account')
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError()
    except ValueError:
        abort(400, 'Invalid amount')

    # Build forward request safely
    gateway_url = os.environ.get('GATEWAY_URL', 'https://example.com/gateway.php')
    payload = {
        'from_account': session['account'],
        'to_account': to_account,
        'amount': amount
    }
    # Forward authenticated transfer request to PHP gateway
    resp = requests.post(gateway_url, json=payload, timeout=5)
    if resp.status_code != 200:
        abort(resp.status_code, 'Transfer failed')

    return jsonify(resp.json())

if __name__ == '__main__':
    app.run(debug=False)
