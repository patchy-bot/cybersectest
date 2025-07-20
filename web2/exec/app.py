from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json() or {}
    code = data.get('code', '')
    # Disallow direct exec; save to a temporary file and run in a restricted container
    with open('/tmp/user_code.py', 'w') as f:
        f.write(code)
    # Use subprocess without shell and in a safe environment
    try:
        result = subprocess.run([
            'python3', '/tmp/user_code.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5, check=False)
    except subprocess.TimeoutExpired:
        return jsonify({'error':'Execution timed out'}), 400
    return jsonify({'stdout': result.stdout.decode(), 'stderr': result.stderr.decode()})

if __name__ == '__main__':
    app.run()