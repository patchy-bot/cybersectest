from flask import Flask, request, jsonify
import sys
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    user_code = request.form.get('code', '')
    # Validate: allow only digits and basic arithmetic
    if not all(c.isdigit() or c in '+-*/() ' for c in user_code):
        return jsonify(error="Invalid characters in code."), 400
    try:
        # Evaluate safely
        result = eval(user_code, {'__builtins__': None}, {})
    except Exception as e:
        return jsonify(error=str(e)), 400
    return jsonify(result=result)

if __name__ == '__main__':
    app.run()
