from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db():
    return psycopg2.connect(dbname='appdb', user='app', password='secret', host='localhost')

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # Parameterized query to prevent SQL injection
    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return jsonify(user)
    return jsonify({'error':'Not found'}), 404

if __name__ == '__main__':
    app.run()