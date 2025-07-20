from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

@app.route('/search', methods=['GET'])
def search():
    user_input = request.args.get('query', '')
    # Use safe query construction without $where
    # For example, search in 'name' field using regex with input sanitized
    import re
    safe_input = re.escape(user_input)  # Escape regex special chars
    query = {"name": {"$regex": safe_input, "$options": "i"}}
    results = list(db.users.find(query))
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False)
