# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced f-string SQL construction with parameterized query using '?'. This prevents injection by treating user input as data.

## Security Notes
Limit term length and sanitize inputs further if needed. Use HTTPS to protect data in transit.

## Fixed Code
```py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = 'app.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search', methods=['GET'])
def search():
    term = request.args.get('term', '')
    # Validate input length
    if len(term) > 100:
        return jsonify({'error': 'Search term too long'}), 400

    conn = get_db_connection()
    # Use parameterized query to avoid SQL injection
    cur = conn.execute('SELECT id, name FROM items WHERE name LIKE ?', (f'%{term}%',))
    rows = cur.fetchall()
    conn.close()

    results = [{'id': row['id'], 'name': row['name']} for row in rows]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
None

## Testing Recommendations
- Attempt SQL injection payloads and verify no data leakage

## Alternative Solutions

### Use SQLAlchemy ORM
**Pros:** Abstracts SQL, Built-in protection
**Cons:** Adds dependency

