from flask import Flask, request, jsonify, session
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin
from werkzeug.security import check_password_hash
import requests
import os

app = Flask(__name__)
# Load secret key from environment variable
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    # TODO: Replace with real user lookup from database
    # Return None if user not found
    return User(user_id, user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    # Retrieve hashed password from secure store
    hashed_password = get_hashed_password(username)
    if not hashed_password or not check_password_hash(hashed_password, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    user = User(username, username)
    login_user(user)
    return jsonify({'message': 'Logged in'}), 200

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.json or {}
    from_account = data.get('from_account')
    to_account = data.get('to_account')
    amount = data.get('amount')
    # Validate input types
    if not isinstance(from_account, str) or not isinstance(to_account, str):
        return jsonify({'error': 'Invalid account identifiers'}), 400
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    # Authorization: ensure the logged-in user owns the from_account
    if current_user.username != from_account:
        return jsonify({'error': 'Unauthorized account access'}), 403
    # Forward request to internal PHP gateway with traceable user context
    gateway_url = os.getenv('GATEWAY_URL', 'http://localhost:8000/gateway.php')
    headers = {
        'X-User-ID': current_user.username,
        'Content-Type': 'application/json'
    }
    payload = {
        'from_account': from_account,
        'to_account': to_account,
        'amount': amount
    }
    resp = requests.post(gateway_url, json=payload, headers=headers, timeout=5)
    return jsonify(resp.json()), resp.status_code


def get_hashed_password(username):
    # TODO: Implement secure retrieval of hashed passwords from database
    return None

if __name__ == '__main__':
    app.run()