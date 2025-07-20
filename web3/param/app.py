from flask import Flask, request, jsonify, session, abort
from itsdangerous import URLSafeTimedSerializer
import requests

app = Flask(__name__)
app.secret_key = 'replace_with_env_secret'
serializer = URLSafeTimedSerializer(app.secret_key)

@app.before_request
def protect_csrf():
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        try:
            serializer.loads(token, max_age=3600)
        except Exception:
            abort(403)

@app.route('/form')
def form():
    token = serializer.dumps('csrf-token')
    return f"<form method='post' action='/forward'>\n" \
           f"<input type='hidden' name='csrf_token' value='{token}'>\n" \
           "<input name='amount'>\n" \
           "<button type='submit'>Send</button>\n" 

@app.route('/forward', methods=['POST'])
def forward():
    amount = request.form.get('amount')
    # Validate amount is a positive integer
    if not amount.isdigit() or int(amount) <= 0:
        return jsonify({'error':'Invalid amount'}),400
    # Forward via POST to gateway
    resp = requests.post('https://example.com/gateway.php', data={'amount': amount}, timeout=5)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run()