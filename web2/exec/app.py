from flask import Flask, request, jsonify
import ast
import sys

app = Flask(__name__)

# Allowed built-in functions for safe evaluation
allowed_builtins = {'abs', 'min', 'max', 'sum', 'sorted', 'len'}

class SafeEval(ast.NodeVisitor):
    def visit(self, node):
        # Allow only select node types (expressions, arithmetic etc.)
        allowed_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Str, ast.NameConstant,
            ast.Call, ast.Name, ast.Load, ast.Compare, ast.BoolOp, ast.List, ast.Tuple,
            ast.Dict, ast.Set, ast.IfExp
        )
        if not isinstance(node, allowed_nodes):
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
        return super().visit(node)

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name) or node.func.id not in allowed_builtins:
            raise ValueError(f"Disallowed function call: {getattr(node.func, 'id', repr(node.func))}")
        for arg in node.args:
            self.visit(arg)

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        code = request.json.get('code')
        if not code:
            return jsonify({'error': 'No code provided'}), 400

        # Parse the code to AST
        tree = ast.parse(code, mode='eval')

        # Validate that the tree contains only safe expressions
        SafeEval().visit(tree)

        # Evaluate the expression safely without builtins
        result = eval(compile(tree, filename='<ast>', mode='eval'), {'__builtins__': {}}, {})

        return jsonify({'result': result})
    except Exception as e:
        # Return error message without exposing sensitive details
        return jsonify({'error': f'Execution failed: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
