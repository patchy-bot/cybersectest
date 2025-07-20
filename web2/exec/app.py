import ast
import flask
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define a whitelist of safe AST nodes
def is_safe_node(node):
    safe_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Str,
        ast.Name, ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.Pow, ast.Mod, ast.Tuple, ast.List
    )
    return isinstance(node, safe_nodes)

# Recursively validate AST
ndef validate_ast(node):
    if not is_safe_node(node):
        raise ValueError(f"Unsafe expression: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        validate_ast(child)

@app.route('/eval', methods=['POST'])
def eval_expr():
    expr = request.json.get('expr', '')
    try:
        # Parse expression into AST
        tree = ast.parse(expr, mode='eval')
        # Validate nodes against whitelist
        validate_ast(tree)
        # Compile and evaluate in restricted namespace
        code_obj = compile(tree, filename='<ast>', mode='eval')
        result = eval(code_obj, {'__builtins__': {}}, {})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
