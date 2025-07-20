# app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
import re

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb

@app.route('/find_user', methods=['GET'])
def find_user():
    username = request.args.get('username', '')
    # Validate allowed username characters
    if not re.match(r'^[A-Za-z0-9_\-]{3,30}$', username):
        return jsonify({'error': 'Invalid username'}), 400

    # Use direct field match instead of $where
    user = db.users.find_one({'username': username}, {'_id': 0, 'username': 1, 'email': 1})
    if not user:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=False)
