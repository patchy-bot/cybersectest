from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    user_code = request.json.get('code', '')
    try:
        # Parse the code safely using ast.literal_eval if expecting literals
        # or restrict to a safe subset of operations
        # Here we reject code execution and only allow arithmetic expressions
        tree = ast.parse(user_code, mode='eval')
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.operator, ast.unaryop)):
                return jsonify({'error': 'Unsafe code detected'}), 400
        result = eval(compile(tree, filename='<ast>', mode='eval'))
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)
