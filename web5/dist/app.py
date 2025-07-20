# web5/dist/app.py
from flask import Flask, request, jsonify, abort
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.getenv('DATABASE_PATH', 'mydb.sqlite')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<username>')
def get_user(username):
    # Enforce username format
    if not username.isalnum():
        abort(400, 'Invalid username')
    conn = get_db_connection()
    # Use parameterized query to prevent SQL injection
    user = conn.execute('SELECT id, username, email FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return jsonify(dict(user))

if __name__ == '__main__':
    app.run()
