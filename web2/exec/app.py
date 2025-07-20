from flask import Flask, request, jsonify, abort
import ast

app = Flask(__name__)

# Allow only safe arithmetic expressions
class SafeEval(ast.NodeVisitor):
    ALLOWED_NODES = {
        ast.Expression, ast.BinOp, ast.UnaryOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
        ast.Num, ast.Constant, ast.Load, ast.USub, ast.UAdd,
    }
    def generic_visit(self, node):
        if type(node) not in self.ALLOWED_NODES:
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
        super().generic_visit(node)

@app.route('/eval', methods=['POST'])
def safe_eval():
    expr = request.json.get('expr')
    if not expr or not isinstance(expr, str):
        abort(400, 'Expression must be a string')
    try:
        # Parse into AST and validate
        tree = ast.parse(expr, mode='eval')
        SafeEval().visit(tree)
        result = eval(compile(tree, '<safe>', 'eval'), {'__builtins__':{}})
        return jsonify({'result': result})
    except Exception as e:
        abort(400, str(e))

if __name__ == '__main__':
    app.run(debug=False)
