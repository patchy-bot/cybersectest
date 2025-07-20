from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/exec', methods=['POST'])
def exec_code():
    user_code = request.json.get('code', '')
    # Only allow single expressions, no statements
    try:
        tree = ast.parse(user_code, mode='eval')
    except SyntaxError:
        return jsonify({'error': 'Invalid syntax: only single expressions allowed'}), 400
    # Whitelist builtins
    safe_builtins = {'abs': abs, 'min': min, 'max': max, 'sum': sum}
    safe_globals = {'__builtins__': safe_builtins}
    try:
        result = eval(compile(tree, '<string>', 'eval'), safe_globals, {})
    except Exception as e:
        return jsonify({'error': 'Execution error', 'details': str(e)}), 400
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)
