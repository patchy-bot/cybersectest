# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed use of `$where` and direct JavaScript injection. Instead, we build a filter object using only allowed fields from query parameters. This prevents arbitrary code execution in MongoDB.

## Security Notes
If range or advanced operators are needed, validate and map them explicitly. Always avoid `$where` unless input is strictly controlled.

## Fixed Code
```py
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb

# Allowed fields for filtering
ALLOWED_FIELDS = {'name', 'age', 'email'}

@app.route('/users', methods=['GET'])
def get_users():
    # Validate and build filter from query parameters
    filters = {}
    for key, value in request.args.items():
        if key in ALLOWED_FIELDS:
            filters[key] = value
        else:
            return jsonify({'error': f'Invalid filter field: {key}'}), 400
    try:
        users = list(db.users.find(filters, {'_id': 0}))
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()

```

## Additional Dependencies
None

## Testing Recommendations
- Attempt NoSQL injection via query string
- Ensure only allowed fields filter the results
- Test with empty and multi-parameter queries

## Alternative Solutions

### Use an ORM/ODM like MongoEngine
**Pros:** Built-in query sanitization, Cleaner models
**Cons:** Additional dependency

