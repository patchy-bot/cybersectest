from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']

@app.route('/search', methods=['GET'])
def search():
    user_input = request.args.get('query', '')
    # Use parameterized query by building a safe query dict
    # Avoid using $where with user input
    query = {"field": {"$regex": f"^{user_input}$", "$options": "i"}}  # Case-insensitive exact match
    results = list(collection.find(query))
    # Convert results to JSON serializable format
    for r in results:
        r['_id'] = str(r['_id'])
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False)
