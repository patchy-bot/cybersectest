from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']

@app.route('/user', methods=['GET'])
def get_user():
    # Validate and cast input to integer
    user_id = request.args.get('id', '')
    if not user_id.isdigit():
        return jsonify({'error': 'Invalid id'}), 400
    uid = int(user_id)
    # Use direct field matching instead of $where
    user = db.users.find_one({'_id': uid}, {'password': 0})
    if not user:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=False)