# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Switched from Python f-strings to `psycopg2` parameterized queries using `%s` placeholders. This prevents SQL injection. Credentials are still plaintext—recommend hashing.

## Security Notes
In production, use environment variables for DB credentials and hashed passwords with a strong algorithm (e.g., bcrypt).

## Fixed Code
```py
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(host='localhost', dbname='users', user='appuser', password='s3cr3t')

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    # Parameterized query to prevent SQL Injection
    cur.execute('SELECT id, role FROM users WHERE username = %s AND password = %s', (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        user_id, role = user
        return jsonify({'user_id': user_id, 'role': role})
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- psycopg2

## Testing Recommendations
- Test login endpoint against SQL injection payloads
- Confirm valid credentials still work
- Review database logs for anomalous queries

## Alternative Solutions

### Use an ORM like SQLAlchemy
**Pros:** Cleaner abstraction, Built-in parameterization
**Cons:** Additional overhead

