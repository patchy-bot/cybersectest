from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    # Parameterized query to prevent SQL Injection
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, username, email FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row)), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run()