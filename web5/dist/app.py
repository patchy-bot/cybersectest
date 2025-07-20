from flask import Flask, request, jsonify, abort
timport sqlite3

app = Flask(__name__)
DB_PATH = 'app.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        abort(400, 'username and password required')
    conn = get_db()
    cursor = conn.cursor()
    # Parameterized query prevents SQL injection
    cursor.execute('SELECT id,username FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    if not user:
        abort(401, 'Invalid credentials')
    return jsonify({'id': user['id'], 'username': user['username']})

if __name__ == '__main__':
    app.run(debug=False)
