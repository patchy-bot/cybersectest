from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)

# Simple token-based authentication for demonstration
VALID_TOKENS = {'user1': 'secrettoken123'}

@app.route('/transfer', methods=['POST'])
def transfer():
    auth_token = request.headers.get('Authorization')
    if not auth_token or auth_token not in VALID_TOKENS.values():
        abort(401, description='Unauthorized')

    # Sanitize and validate POST data
    data = request.get_json(force=True)
    if not data or 'amount' not in data or 'recipient' not in data:
        abort(400, description='Invalid input')

    amount = data['amount']
    recipient = data['recipient']

    # Basic input validation
    if not isinstance(amount, (int, float)) or amount <= 0:
        abort(400, description='Invalid amount')
    if not isinstance(recipient, str) or len(recipient) == 0:
        abort(400, description='Invalid recipient')

    # Forward sanitized data to internal PHP gateway
    try:
        response = requests.post('http://localhost/web3/param/gateway.php', json={'amount': amount, 'recipient': recipient})
        response.raise_for_status()
    except requests.RequestException as e:
        abort(502, description='Internal gateway error')

    return jsonify({'status': 'Transfer request forwarded'}), 200

if __name__ == '__main__':
    app.run(debug=False)
