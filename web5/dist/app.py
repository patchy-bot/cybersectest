# web5/dist/app.py
import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
conn = sqlite3.connect('users.db', check_same_thread=False)
conn.row_factory = sqlite3.Row

@app.route('/user', methods=['GET'])
def get_user():
    name = request.args.get('name', '')
    if not name:
        abort(400, description='Missing name')
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT id, name, email FROM users WHERE name = ?', (name,))
    row = cursor.fetchone()
    if not row:
        abort(404, description='User not found')
    user = {'id': row['id'], 'name': row['name'], 'email': row['email']}
    return jsonify(user), 200

if __name__ == '__main__':
    app.run(debug=False)