from flask import Flask, request, jsonify, session, abort
from flask_wtf import CSRFProtect
from functools import wraps

app = Flask(__name__)
app.secret_key = 'ReplaceWithStrongSecret!'
csrf = CSRFProtect(app)

# Mock user store
def current_user():
    user_id = session.get('user_id')
    return user_id

# Simple login_required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user():
            abort(401)
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Replace with real authentication
    if data.get('user_id'):
        session['user_id'] = data['user_id']
        return jsonify({'status': 'logged in'})
    return jsonify({'error': 'login failed'}), 400

@app.route('/transfer', methods=['POST'])
@csrf.exempt  # if using JS clients, ensure CSRF token is passed; here for example
@login_required
def transfer():
    data = request.get_json()
    from_acc = data.get('from')
    to_acc = data.get('to')
    amount = data.get('amount', 0)
    # Business logic checks
    if current_user() != from_acc:
        return jsonify({'error': 'Unauthorized: cannot transfer from this account'}), 403
    if amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    accounts = get_accounts()
    if accounts.get(from_acc, 0) < amount:
        return jsonify({'error': 'Insufficient funds'}), 400
    # Perform transaction atomically
    accounts[from_acc] -= amount
    accounts[to_acc] = accounts.get(to_acc, 0) + amount
    save_accounts(accounts)
    return jsonify({'status': 'success'}), 200
