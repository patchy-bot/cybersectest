from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.testdb

@app.route('/search', methods=['GET'])
def search_user():
    username = request.args.get('username', '')
    # Input validation: only allow alphanumeric usernames
    if not username.isalnum():
        return jsonify({'error':'Invalid username'}), 400
    # Use safe query builder without $where
    user = db.users.find_one({'username': username})
    if not user:
        return jsonify({'error':'Not found'}), 404
    user['_id'] = str(user['_id'])
    return jsonify(user)

if __name__ == '__main__':
    app.run()