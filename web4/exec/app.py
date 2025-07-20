# web4/exec/app.py
from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
import os

app = Flask(__name__)
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URI)
db = client.mydb

@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('user', '')
    if not username.isalnum():
        abort(400, 'Invalid username format')
    # Use a parameterized query rather than $where
    user = db.users.find_one({'username': username}, {'_id': 0, 'data': 1})
    if not user:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run()
