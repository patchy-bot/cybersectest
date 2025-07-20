from flask import Flask, request, jsonify, session, abort
from functools import wraps
import os
import requests

app = Flask(__name__)
# SECRET_KEY must be set as an environment variable in production
env_secret = os.getenv('SECRET_KEY')
if not env_secret:
    raise RuntimeError("SECRET_KEY environment variable not set")
app.secret_key = env_secret

# Simple session-based authentication decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            abort(401)
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    # TODO: validate credentials against user store
    if username == 'demo' and password == 'demo':
        session['user_id'] = username
        return jsonify({'status':'logged_in'})
    abort(401)

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.get_json() or {}
    amount = data.get('amount')
    to_account = data.get('to_account')
    # Input validation
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    if not isinstance(to_account, str) or not to_account.isalnum():
        return jsonify({'error': 'Invalid destination account'}), 400
    # Forward to PHP gateway with the authenticated user_id
    payload = {
        'from_user': session['user_id'],
        'to_account': to_account,
        'amount': amount
    }
    resp = requests.post('https://yourdomain.com/web3/param/gateway.php', json=payload, timeout=5)
    return (resp.text, resp.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)