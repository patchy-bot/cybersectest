# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed use of MongoDB $where with raw input and replaced it with a direct filter on the 'key' field. Added validation to allow only alphanumeric keys.

## Security Notes
Avoid any use of $where or JavaScript evaluation. Always build queries using safe filters or parameterized query builders.

## Fixed Code
```py
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
db = client.challenge_db
collection = db.flags

@app.route('/find', methods=['GET'])
def find_flag():
    key = request.args.get('key', '')
    # Validate that key is alphanumeric without any special operators
    if not key.isalnum():
        return jsonify({'error': 'Invalid key format'}), 400
    # Use a parameterized filter instead of $where
    doc = collection.find_one({'key': key, 'published': 1}, {'flag': 0})
    if not doc:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'key': doc['key'], 'other_data': doc.get('other_data')})

if __name__ == '__main__':
    app.run()

```

## Additional Dependencies
- os

## Testing Recommendations
- Attempt injection via ?key=$where and verify rejection
- Query valid keys and invalid keys

## Alternative Solutions
None provided
