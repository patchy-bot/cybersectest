# web5/src/app.py
from flask import Flask, request, jsonify, abort
import psycopg2
import os

app = Flask(__name__)
DB_DSN = os.getenv('DATABASE_DSN', 'dbname=mydb user=app password=secret host=localhost')

def get_conn():
    return psycopg2.connect(DB_DSN)

@app.route('/account/<account_id>')
def get_account(account_id):
    # Validate numeric account ID
    if not account_id.isdigit():
        abort(400, 'Invalid account ID')
    conn = get_conn()
    cur = conn.cursor()
    # Parameterized query
    cur.execute('SELECT id, balance FROM accounts WHERE id = %s', (int(account_id),))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        abort(404)
    return jsonify({'id': row[0], 'balance': row[1]})

if __name__ == '__main__':
    app.run()
