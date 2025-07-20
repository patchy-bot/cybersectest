from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Whitelist of safe AST node types
SAFE_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,
    ast.operator,
    ast.unaryop,
    ast.Expr,
    ast.Load,
    ast.Constant
)


def is_safe_node(node):
    return isinstance(node, SAFE_NODES)


def safe_eval(expr: str) -> float:
    """
    Parse and evaluate a mathematical expression safely using AST.
    Only allows numeric literals and basic arithmetic operators.
    """
    # Parse expression as AST in 'eval' mode
    tree = ast.parse(expr, mode='eval')
    # Walk the AST and reject any unsafe nodes
    for node in ast.walk(tree):
        if not is_safe_node(node):
            raise ValueError(f"Unsafe expression: {type(node).__name__}")
    # Compile and evaluate in an empty context
    code = compile(tree, '<input>', 'eval')
    return eval(code, {'__builtins__': {}}, {})

@app.route('/exec', methods=['POST'])
def execute():
    # Only allow simple math expressions
    user_code = request.form.get('code', '')
    try:
        result = safe_eval(user_code)
        return jsonify({ 'result': result })
    except Exception as e:
        return jsonify({ 'error': str(e) }), 400

if __name__ == '__main__':
    app.run(debug=False)
