from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)
VALID_ACTIONS = {'create', 'update', 'delete'}

@app.route('/proxy', methods=['POST'])
def proxy_to_gateway():
    data = request.get_json()
    if not data or 'action' not in data or data['action'] not in VALID_ACTIONS:
        abort(400, 'Invalid or missing action')
    # Whitelist parameters per action
    payload = {'action': data['action']}
    if data['action'] == 'update':
        user_id = data.get('user_id')
        if not isinstance(user_id, int):
            abort(400, 'user_id must be integer')
        payload['user_id'] = user_id
        payload['value'] = str(data.get('value',''))[:100]
    # Forward only whitelisted fields
    resp = requests.post('https://gateway.example.com/gateway.php', json=payload, timeout=5)
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(debug=False)
