from flask import Flask, request, jsonify
from pymongo import MongoClient
import re

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.usersdb

@app.route('/find', methods=['GET'])
def find_user():
    username = request.args.get('username', '')
    # Validate username: allow alphanumeric only
    if not re.match(r'^[a-zA-Z0-9_]{1,32}$', username):
        return jsonify(error="Invalid username"), 400
    user = db.users.find_one({'username': username}, {'_id': 0})
    if not user:
        return jsonify(error="Not found"), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run()
