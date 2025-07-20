import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    if not user_id or not user_id.isdigit():
        return jsonify({'error': 'Invalid user id'}), 400
    conn = psycopg2.connect(dbname='mydb', user='user', password='pass', host='localhost')
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify({'id': user[0], 'name': user[1]})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)
