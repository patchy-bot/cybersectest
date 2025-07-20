from flask import Flask, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'REPLACE_WITH_SECURE_RANDOM'

@app.route('/login', methods=['POST'])
def login():
    # Validate input
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    # Perform local auth or proxy with credentials header
    resp = requests.post('https://backend.local/auth', json={'user': username, 'pass': password})
    if resp.status_code == 200:
        session['user'] = username
        return redirect(url_for('dashboard'))
    return 'Login failed', 401

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f'Welcome, {session["user"]}!'

if __name__ == '__main__':
    app.run(debug=False)