# This file mirrors src/app.py but is the distribution build
from flask import Flask, request, abort, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/flag', methods=['GET'])
def get_flag():
    username = request.args.get('username', '').strip()
    if not username:
        abort(400, 'Username required')

    # Parameterized query to prevent SQL injection
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT flag FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({'flag': row['flag']})
    abort(404, 'User not found')

if __name__ == '__main__':
    app.run(debug=False)
