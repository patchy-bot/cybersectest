from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')

    # Input validation: ensure user_id is numeric
    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user ID'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify(dict(user)), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)
