import sqlite3
from flask import Flask, request, abort

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/transact', methods=['POST'])
def transact():
    user = request.form.get('user', '').strip()
    amount = request.form.get('amount', '').strip()
    try:
        amt = float(amount)
    except ValueError:
        abort(400, 'Invalid amount')
    conn = get_db_connection()
    # Use parameterized queries to prevent SQL injection
    conn.execute(
        'UPDATE accounts SET balance = balance + ? WHERE user = ?',
        (amt, user)
    )
    conn.commit()
    conn.close()
    return 'OK', 200

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    conn = get_db_connection()
    # Parameterized SELECT
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()
    conn.close()
    if user:
        return 'Logged in', 200
    else:
        return 'Authentication failed', 401

if __name__ == '__main__':
    app.run()