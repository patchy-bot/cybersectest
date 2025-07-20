from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db = client.shop

@app.route('/items', methods=['GET'])
def get_items():
    category = request.args.get('category', '')
    # Use direct field match instead of $where JavaScript
    results = list(db.items.find({'category': category}, {'_id': 0}))
    return jsonify(results)

if __name__ == '__main__':
    app.run()