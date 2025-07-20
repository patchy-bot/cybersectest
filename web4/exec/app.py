from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']

@app.route('/search', methods=['GET'])
def search():
    username = request.args.get('username', '')

    # Input validation: allow only alphanumeric usernames
    if not username.isalnum():
        return jsonify({'error': 'Invalid username'}), 400

    # Use parameterized query without $where to prevent NoSQL injection
    result = collection.find_one({'username': username})

    if result:
        return jsonify({'user': result}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)
