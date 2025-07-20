from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.users_db

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username', '')
    # Validate username: allow only alphanumerics and underscores
    if not username.isalnum():
        return jsonify({'error':'Invalid username'}),400
    # Use a safe query builder without $where
    user = db.users.find_one({'username': username}, {'_id':0, 'username':1, 'email':1})
    if not user:
        return jsonify({'error':'Not found'}),404
    return jsonify(user)

if __name__ == '__main__':
    app.run()