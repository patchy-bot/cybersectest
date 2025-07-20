from flask import Flask, request, jsonify
def get_db_connection():
    import sqlite3
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id', '')
    if not user_id.isdigit():
        return jsonify(error="Invalid id"), 400
    conn = get_db_connection()
    cur = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cur.execute('SELECT name, email FROM users WHERE id = ?', (int(user_id),))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(name=row['name'], email=row['email'])
    else:
        return jsonify(error="Not found"), 404

if __name__ == '__main__':
    app.run()
