# Security Fix for web3/param/app.py

**Vulnerability Type:** AUTHORIZATION_FAILURE  
**Confidence Level:** MEDIUM  
**Breaking Changes:** No

## Original Issue
Added login endpoint with session-based authentication and CSRF token stored in session. Transfer endpoint now checks session user and CSRF token, preventing unauthorized transfers.

## Security Notes
In production, use HTTPS, secure cookies, password hashing and persistent user store.

## Fixed Code
```py
from flask import Flask, request, session, redirect, url_for, abort
from gateway import transfer
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Simple in-memory user store for demo
USERS = {'alice':'password123','bob':'password456'}

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('user')
    pwd = request.form.get('password')
    if USERS.get(user) == pwd:
        session['user'] = user
        session['csrf_token'] = secrets.token_hex(16)
        return 'Logged in'
    abort(401)

@app.route('/transfer', methods=['POST'])
def make_transfer():
    if 'user' not in session:
        abort(401)
    # CSRF protection
    token = request.form.get('csrf_token')
    if not token or token != session.get('csrf_token'):
        abort(403)
    from_user = session['user']
    to_user = request.form.get('to')
    amount = request.form.get('amount')
    try:
        amt = float(amount)
    except ValueError:
        abort(400)
    # Call gateway with authenticated user
    result = transfer(from_user, to_user, amt)
    return result

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- secrets

## Testing Recommendations
- Attempt transfer without login
- Attempt with invalid CSRF token

## Alternative Solutions
None provided
