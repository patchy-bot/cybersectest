from flask import Flask, request, abort

app = Flask(__name__)
# In production, replace with real user-store and secure tokens
VALID_TOKENS = {
    'alice': 'token_alice_123',
    'bob': 'token_bob_456'
}

@app.before_request
def check_auth():
    if request.endpoint == 'pay':
        token = request.headers.get('X-API-Key', '')
        if not token or token not in VALID_TOKENS.values():
            abort(401, 'Invalid or missing API key')

@app.route('/pay', methods=['POST'])
def pay():
    payer = request.form.get('from', '')
    token = request.headers.get('X-API-Key', '')
    # Ensure token matches declared payer
    if VALID_TOKENS.get(payer) != token:
        abort(403, 'Token does not match payer')
    payee = request.form.get('to', '')
    try:
        amount = float(request.form.get('amount', '0'))
    except ValueError:
        abort(400, 'Invalid amount')
    # perform transaction logic here
    return 'Done', 200

if __name__ == '__main__':
    app.run()