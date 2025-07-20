from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Define a whitelist of safe names/functions
SAFE_NAMES = {
    'abs': abs,
    'max': max,
    'min': min
}

class SafeEval(ast.NodeVisitor):
    def visit(self, node):
        if isinstance(node, ast.Call):
            if not (isinstance(node.func, ast.Name) and node.func.id in SAFE_NAMES):
                raise ValueError(f"Use of unsafe function {node.func.id}")
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST): self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)

@app.route('/eval', methods=['POST'])
def evaluate():
    data = request.json.get('code', '')
    try:
        tree = ast.parse(data, mode='eval')
        SafeEval().visit(tree)
        # Only evaluate safe expressions
        result = eval(compile(tree, filename='<ast>', mode='eval'), {'__builtins__': {}}, SAFE_NAMES)
        return jsonify(result=result)
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run()