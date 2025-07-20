from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db():
    return psycopg2.connect(dbname='app', user='user', password='pass', host='localhost')

@app.route('/item')
def get_item():
    sku = request.args.get('sku', '')
    # Allow only alphanumeric skus
    if not sku.isalnum():
        return jsonify(error="Invalid SKU"), 400
    conn = get_db()
    cur = conn.cursor()
    # Use parameterized queries
    cur.execute("SELECT name, price FROM items WHERE sku = %s", (sku,))
    item = cur.fetchone()
    conn.close()
    if item:
        return jsonify(name=item[0], price=item[1])
    return jsonify(error="Not found"), 404

if __name__ == '__main__':
    app.run()