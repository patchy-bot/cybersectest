from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Simulated user session or token (in real cases use proper auth)
current_user = {'username': 'alice', 'authorized_accounts': ['alice']}

balances = {
    'alice': 1000,
    'bob': 500
}

@app.route('/transfer', methods=['POST'])
def transfer_funds():
    sender = request.json.get('sender')
    recipient = request.json.get('recipient')
    amount = request.json.get('amount')

    # Validate input types and content
    if not isinstance(sender, str) or not isinstance(recipient, str):
        return jsonify({'error': 'Sender and recipient must be strings'}), 400
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Amount must be positive number'}), 400

    # Authorization check: Only allow current_user to transfer from their own authorized accounts
    if sender not in current_user['authorized_accounts']:
        return abort(403, description='Unauthorized to transfer from this account')

    # Check balance
    if balances.get(sender, 0) < amount:
        return jsonify({'error': 'Insufficient balance'}), 400

    # Enforce recipient exists
    if recipient not in balances:
        return jsonify({'error': 'Recipient does not exist'}), 400

    # Perform the transfer
    balances[sender] -= amount
    balances[recipient] += amount

    return jsonify({'message': 'Transfer successful', 'balances': balances})

if __name__ == '__main__':
    app.run(debug=True)
