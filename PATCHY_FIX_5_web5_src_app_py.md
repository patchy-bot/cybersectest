# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Switched from f-string to parameterized SQL via psycopg2. Added validation to ensure id is numeric before passing to query.

## Security Notes
Ensure DATABASE_URL is set in environment. Use connection pooling for production.

## Fixed Code
```py
from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)
DB_DSN = os.getenv('DATABASE_URL')

def get_db_connection():
    return psycopg2.connect(DB_DSN)

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id', '')
    # Validate that id is integer
    if not user_id.isdigit():
        return jsonify({'error': 'Invalid user id'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    # Parameterized query
    cur.execute('SELECT id, username, email FROM users WHERE id = %s', (int(user_id),))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': row[0], 'username': row[1], 'email': row[2]})

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- os

## Testing Recommendations
- Test with non-numeric ids
- Test SQL injection patterns in id parameter

## Alternative Solutions

### Use an ORM like SQLAlchemy
**Pros:** Less raw SQL, Maintained models
**Cons:** Additional learning curve

