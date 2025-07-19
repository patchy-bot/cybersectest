# Security Fix for web5/dist/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced f-string SQL construction with parameterized queries using `?` placeholders. This ensures user input is never directly concatenated into SQL and guards against injection attacks.

## Security Notes
Do not store plaintext passwords in production. Use salted hashing (e.g., bcrypt).

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT id, role FROM users WHERE username = ? AND password = ?', (username, password))
    row = cursor.fetchone()
    conn.close()
    if row:
        user_id, role = row
        return jsonify({'user_id': user_id, 'role': role})
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
None

## Testing Recommendations
- Attempt login with SQL injection payload
- Verify normal logins still succeed
- Run automated SQLi scanner

## Alternative Solutions

### Use an ORM like SQLAlchemy
**Pros:** Automates parameterization, Easier migrations
**Cons:** Additional learning curve

