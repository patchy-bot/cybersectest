import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    # Validate that id is numeric
    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user ID'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    # Use parameterized query to prevent injection
    cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row)), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)