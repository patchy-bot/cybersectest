import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = 'app.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/items', methods=['GET'])
def list_items():
    conn = get_db()
    items = conn.execute("SELECT id, name, price FROM items").fetchall()
    conn.close()
    return jsonify([dict(row) for row in items])

@app.route('/item', methods=['GET'])
def get_item():
    item_id = request.args.get('id')
    if not item_id or not item_id.isdigit():
        return jsonify({'error': 'Invalid item ID'}), 400
    conn = get_db()
    # Parameterized query
    row = conn.execute("SELECT id, name, price FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)