# app.py
import requests
from flask import Flask, request, jsonify, session, redirect, url_for
import re

app = Flask(__name__)
app.secret_key = 'replace-with-secure-random'

ACCOUNT_REGEX = re.compile(r'^[A-Z0-9]{10,20}$')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # authenticate user (omitted)
    session['user'] = username
    return redirect(url_for('transfer_money'))

@app.route('/transfer', methods=['POST'])
def transfer_money():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    amount = request.json.get('amount')
    target = request.json.get('target_account')

    # Input validation
    try:
        amount = int(amount)
        if amount <= 0 or amount > 100000:
            raise ValueError
    except Exception:
        return jsonify({'error': 'Invalid amount'}), 400

    if not isinstance(target, str) or not ACCOUNT_REGEX.match(target):
        return jsonify({'error': 'Invalid account number'}), 400

    # Forward sanitized payload
    resp = requests.post(
        'https://api.example.com/gateway.php',
        json={'amount': amount, 'target_account': target},
        cookies={'PHPSESSID': session.get('PHPSESSID')}
    )
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(debug=False)