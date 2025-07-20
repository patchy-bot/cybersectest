from flask import Flask, request, jsonify, session, redirect, url_for
from functools import wraps
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

# Simple in-memory user store
USERS = {'alice': 'password123'}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if USERS.get(user) == pw:
            session['username'] = user
            return redirect(url_for('balance'))
        return 'Invalid credentials', 403
    return '''<form method=post>username:<input name=username>password:<input name=password type=password><input type=submit></form>'''

@app.route('/balance')
@login_required
def balance():
    user = session['username']
    # Fetch from backend with authenticated user context
    bal = 1000  # placeholder
    return jsonify(user=user, balance=bal)

if __name__ == '__main__':
    app.run()