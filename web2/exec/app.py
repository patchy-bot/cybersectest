# app.py
from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Define a safe namespace for evaluation
SAFE_GLOBALS = {
    '__builtins__': None,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    # add other safe functions as needed
}
SAFE_LOCALS = {}

@app.route('/evaluate', methods=['POST'])
def evaluate_expression():
    data = request.get_json()
    expr = data.get('expr', '')
    if not isinstance(expr, str) or len(expr) > 200:
        return jsonify({'error': 'Invalid expression'}), 400
    try:
        # Parse expression into AST and ensure it's an expression node
        node = ast.parse(expr, mode='eval')
        # Only allow literal and safe operators
        for sub in ast.walk(node):
            if not isinstance(sub, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                     ast.Num, ast.Name, ast.Load,
                                     ast.Add, ast.Sub, ast.Mult, ast.Div,
                                     ast.Pow, ast.Mod, ast.USub)):
                return jsonify({'error': 'Unsupported operation'}), 400
        result = eval(compile(node, filename='<ast>', mode='eval'), SAFE_GLOBALS, SAFE_LOCALS)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': 'Evaluation error'}), 400

if __name__ == '__main__':
    app.run(debug=False)