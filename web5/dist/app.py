import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    # Use parameterized query to prevent SQL injection
    conn = get_db_connection()
    cur = conn.execute('SELECT id, username, email FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify({
            'id': row['id'],
            'username': row['username'],
            'email': row['email']
        })
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)
