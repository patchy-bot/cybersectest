# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced f-string SQL construction with a parameterized query using '?' placeholder. Added input validation to allow only alphanumeric and underscore in usernames.

## Security Notes
Always use parameterized queries to prevent SQL injection. Validate inputs against an allowlist for additional defense in depth.

## Fixed Code
```py
from flask import Flask, request, jsonify
t import sqlite3, os

app = Flask(__name__)
DB_PATH = os.getenv('DB_PATH', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user/<username>')
def get_user(username):
    # Validate username: allow only alphanumeric and underscores
    if not username.replace('_','').isalnum():
        return jsonify({'error': 'Invalid username'}), 400
    conn = get_db_connection()
    cursor = conn.execute('SELECT id, username, email FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run()

```

## Additional Dependencies
- sqlite3
- os

## Testing Recommendations
- Attempt SQL injection payloads in username and verify failure
- Fetch valid usernames and verify correct responses

## Alternative Solutions
None provided
