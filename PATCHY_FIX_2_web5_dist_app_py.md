# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced f-string query with a parameterized SQLite query (`?` placeholder) to prevent SQL injection.

## Security Notes
Always use parameterized queries for user-supplied data. Avoid string concatenation for SQL.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
DB_PATH = 'data.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<username>')
def get_user(username):
    conn = get_db()
    cursor = conn.cursor()
    # Use parameterized query to prevent injection
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        abort(404)
    return jsonify(dict(row))

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
None

## Testing Recommendations
- Attempt username="' OR '1'='1" and confirm no data leakage

## Alternative Solutions
None provided
