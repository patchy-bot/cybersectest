# Security Fix for web4/exec/app.py

**Vulnerability Type:** NOSQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed use of `$where` JavaScript injection. Instead, we whitelist searchable fields and construct a safe regex query. No user-supplied code executes on the server.

## Security Notes
Monitor regex performance to avoid ReDoS. Consider rate-limiting.

## Fixed Code
```py
from flask import Flask, request, jsonify, abort
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.appdb

@app.route('/search')
def search():
    # Validate and whitelist field names
    allowed_fields = {'username', 'email'}
    field = request.args.get('field')
    if field not in allowed_fields:
        abort(400, 'Invalid field')
    value = request.args.get('q', '')
    # Build safe query
    query = {field: {'$regex': f'^{value}', '$options': 'i'}}
    results = list(db.users.find(query, {'_id':0}))
    return jsonify(results)

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
None

## Testing Recommendations
- Attempt injection via field name
- Test special regex patterns

## Alternative Solutions
None provided
