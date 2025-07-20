# app.py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    # Validate username
    if not isinstance(username, str) or len(username) > 30:
        return jsonify({'error': 'Invalid username'}), 400

    db = get_db()
    # Parameterized query to prevent SQL injection
    cursor = db.execute('SELECT username, email, created_at FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(row))

if __name__ == '__main__':
    app.run(debug=False)