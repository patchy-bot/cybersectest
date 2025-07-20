import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to database
conn = sqlite3.connect('app.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/get_user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user id'}), 400

    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'id': user[0], 'name': user[1], 'email': user[2]})

if __name__ == '__main__':
    app.run(debug=True)
