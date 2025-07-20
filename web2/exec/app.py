# web2/exec/app.py
from flask import Flask, request, jsonify
import ast
import operator as op

# Whitelist of allowed operators
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def safe_eval(expr):
    """
    Safely evaluate a mathematical expression using AST parsing.
    Prevents arbitrary code execution by only allowing basic operators and numeric literals.
    """
    def _eval(node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        if isinstance(node, ast.BinOp):  # <left> <operator> <right>
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](_eval(node.left), _eval(node.right))
            raise ValueError(f"Operator {op_type} not allowed")
        if isinstance(node, ast.UnaryOp):  # -<operand>
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](_eval(node.operand))
            raise ValueError(f"Operator {op_type} not allowed")
        raise ValueError(f"Unsupported expression: {node}")

    node = ast.parse(expr, mode='eval').body
    return _eval(node)

app = Flask(__name__)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    expr = data.get('expression', '')
    try:
        result = safe_eval(expr)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    app.run(debug=False)
