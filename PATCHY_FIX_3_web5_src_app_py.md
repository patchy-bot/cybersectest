# Security Fix for web5/src/app.py

**Vulnerability Type:** SQL_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaced f-string built query with parameterized `?` placeholder. Added basic numeric validation to ensure id is digit.

## Security Notes
Further harden by casting to int and using strict types.

## Fixed Code
```py
import sqlite3
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
DB = 'app.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/item')
def get_item():
    item_id = request.args.get('id')
    if not item_id or not item_id.isdigit():
        abort(400, 'Invalid id')
    conn = get_db()
    cur = conn.cursor()
    # Parameterized query
    cur.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = cur.fetchone()
    conn.close()
    if not item:
        abort(404)
    return jsonify(dict(item))

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
None

## Testing Recommendations
- Test with id parameters containing SQL meta-characters

## Alternative Solutions
None provided
