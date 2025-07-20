import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    # Parameterized query to prevent SQL injection
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, username FROM users WHERE username = ? AND password_hash = ?',
                (username, password))
    user = cur.fetchone()
    conn.close()
    if user:
        return jsonify({'status':'ok','user': dict(user)})
    return jsonify({'status':'fail'}),401

if __name__ == '__main__':
    app.run()