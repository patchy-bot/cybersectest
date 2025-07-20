from flask import Flask, request, jsonify
import ast
import operator

app = Flask(__name__)

# Only allow a safe subset of AST nodes and operators for arithmetic expressions
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

class SafeEvaluator(ast.NodeVisitor):
    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type} not allowed")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Operator {op_type} not allowed")

    def visit_Num(self, node):  # for Python <3.8
        return node.n

    def visit_Constant(self, node):  # for Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only int/float constants are allowed")

    def generic_visit(self, node):
        raise ValueError(f"Disallowed expression: {type(node)}")

@app.route('/calculate', methods=['POST'])
def calculate():
    expr = request.form.get('code', '')
    try:
        # Parse into AST and ensure only safe nodes
        tree = ast.parse(expr, mode='eval')
        evaluator = SafeEvaluator()
        result = evaluator.visit(tree)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)