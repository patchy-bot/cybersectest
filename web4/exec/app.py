from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.users_db

@app.route('/users', methods=['GET'])
def get_users():
    # Accept only specific query parameters, avoid $where entirely
    username = request.args.get('username')
    age = request.args.get('age', type=int)
    query = {}
    if username:
        # simple exact match
        query['username'] = username
    if age is not None:
        query['age'] = age
    # Return only needed fields
    users = list(db.users.find(query, {'_id': 0, 'password': 0}))
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=False)
