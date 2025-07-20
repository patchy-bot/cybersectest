import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database connection
conn = sqlite3.connect('app.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/search', methods=['GET'])
def search_users():
    q = request.args.get('q', '')
    if not q:
        return jsonify({'error': 'Missing query parameter'}), 400

    # Using parameterized query with LIKE to prevent SQL injection
    like_query = f'%{q}%'
    cursor.execute('SELECT id, name FROM users WHERE name LIKE ?', (like_query,))
    results = cursor.fetchall()

    users = [{'id': row[0], 'name': row[1]} for row in results]
    return jsonify({'results': users})

if __name__ == '__main__':
    app.run(debug=True)
