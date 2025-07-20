from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.mydb

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id', '')
    # Validate ObjectId format
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({'error': 'Invalid id format'}), 400

    # Use safe query object, no $where
    user = db.users.find_one({'_id': oid}, {'password': 0})
    if not user:
        return jsonify({'error': 'Not found'}), 404
    user['_id'] = str(user['_id'])
    return jsonify(user)

if __name__ == '__main__':
    app.run()