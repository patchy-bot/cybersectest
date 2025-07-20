import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = get_db()
    cur = conn.cursor()
    # Parameterized query to prevent injection
    cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cur.fetchone()
    if user:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'fail'}), 401
