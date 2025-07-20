from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.mydb

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    if not username.isalnum():
        abort(400, 'Invalid username')
    # Use field equality instead of $where
    user = db.users.find_one({'username': username}, {'_id':0, 'username':1, 'email':1})
    if not user:
        abort(404, 'User not found')
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=False)
