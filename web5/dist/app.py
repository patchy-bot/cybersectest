from flask import Flask, request, jsonify
def get_db():
    import sqlite3
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/user')
def user():
    username = request.args.get('username', '')
    conn = get_db()
    cur = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cur.execute('SELECT id, email FROM users WHERE username = ?', (username,))
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({'id': row['id'], 'email': row['email']})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)