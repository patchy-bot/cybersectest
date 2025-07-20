from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/items')
def items():
    search = request.args.get('search', '')
    conn = get_db()
    # Use parameterized query
    cur = conn.execute('SELECT id, name, price FROM items WHERE name LIKE ?', ('%'+search+'%',))
    rows = cur.fetchall()
    result = [dict(r) for r in rows]
    return jsonify(result)

if __name__ == '__main__':
    app.run()