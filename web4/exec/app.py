# web4/exec/app.py
from flask import Flask, request, jsonify, abort
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb

# Allowlist of searchable fields
ALLOWED_FIELDS = {'username', 'email', 'age'}

@app.route('/find', methods=['GET'])
def find():
    field = request.args.get('field')
    value = request.args.get('value')
    # Validate field name
    if field not in ALLOWED_FIELDS:
        abort(400, description='Invalid search field')
    # Build safe query
    query = {field: value}
    results = list(db.users.find(query, {'_id': 0}))
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=False)