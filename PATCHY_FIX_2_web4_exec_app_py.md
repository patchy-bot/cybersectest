# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed use of $where with unsanitized input. Now uses direct field query with validation on username (alphanumeric).

## Security Notes
Further tighten input validation depending on username policy. Use indexing on username for performance.

## Fixed Code
```py
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
db = client['mydb']
users = db['users']

@app.route('/user', methods=['GET'])
def get_user():
    # Only allow lookup by exact username
    username = request.args.get('username', '')
    if not username.isalnum():
        return jsonify({'error': 'Invalid username'}), 400

    user = users.find_one({'username': username}, {'_id':0, 'username':1, 'email':1})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- os

## Testing Recommendations
- Attempt injection via special characters
- Verify existing valid usernames still retrievable

## Alternative Solutions

### Use a query builder or ODM (e.g. mongoengine)
**Pros:** Stronger abstraction, Built-in sanitization
**Cons:** Additional dependency, Learning curve

