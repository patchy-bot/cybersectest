from flask import Flask, request, jsonify, abort
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb

@app.route('/users', methods=['GET'])
def get_user():
    name = request.args.get('name', '').strip()
    if not name:
        abort(400, 'Missing name parameter')
    # Parameterized query: no $where
    user = db.users.find_one({'name': name}, {'_id': 0})
    return jsonify(user or {})

@app.route('/products', methods=['POST'])
def filter_products():
    data = request.get_json() or {}
    query = {}
    # Whitelist permitted filters
    if 'category' in data:
        query['category'] = data['category']
    if 'price_min' in data:
        try:
            query['price'] = {'$gte': float(data['price_min'])}
        except ValueError:
            abort(400, 'Invalid price_min')
    results = list(db.products.find(query, {'_id': 0}))
    return jsonify(results)

if __name__ == '__main__':
    app.run()