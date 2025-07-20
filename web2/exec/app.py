from flask import Flask, request, jsonify
import ast
import operator as op

app = Flask(__name__)

# Supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv}

def eval_expr(node):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        left = eval_expr(node.left)
        right = eval_expr(node.right)
        return operators[type(node.op)](left, right)
    else:
        raise ValueError("Unsupported expression")

@app.route('/calc', methods=['POST'])
def calc():
    data = request.get_json()
    expr = data.get('expr', '')
    try:
        # Parse expression into AST and evaluate safely
        node = ast.parse(expr, mode='eval').body
        result = eval_expr(node)
        return jsonify({'result': result})
    except Exception:
        return jsonify({'error': 'Invalid expression'}), 400

if __name__ == '__main__':
    app.run(debug=False)