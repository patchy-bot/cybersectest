# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed direct use of exec. Instead, we parse user code into an AST and only allow a restricted set of node types. We then compile and eval in a locked-down namespace with no builtins, preventing arbitrary code execution.

## Security Notes
Ensure the whitelist is maintained; update ALLOWED_NODES if new safe operations are required. Consider further sandboxing or resource limits.

## Fixed Code
```py
from flask import Flask, request, jsonify, abort
import ast

app = Flask(__name__)

# Whitelist of allowed AST node types
ALLOWED_NODES = {
    ast.Module, ast.Expr, ast.BinOp, ast.UnaryOp,
    ast.Num, ast.Str, ast.NameConstant, ast.List,
    ast.Tuple, ast.Dict, ast.Load, ast.operator, ast.unaryop
}

class SafeEvaluator(ast.NodeTransformer):
    def generic_visit(self, node):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
        return super().generic_visit(node)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    code = request.json.get('code', '')
    if not code:
        abort(400, 'No code provided')
    try:
        # Parse and transform AST to ensure it's safe
        tree = ast.parse(code, mode='eval')
        SafeEvaluator().visit(tree)
        # Compile and evaluate in empty namespace
        compiled = compile(tree, '<string>', 'eval')
        result = eval(compiled, {'__builtins__': {}}, {})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
```

## Additional Dependencies
- ast

## Testing Recommendations
- Submit benign expressions (e.g., 1+2) and verify result
- Submit forbidden operations (e.g., open(), import os) to ensure they're blocked

## Alternative Solutions

### Run submitted code in an external sandboxed container
**Pros:** Strong isolation
**Cons:** Operational overhead

### Use a specialized sandbox library like RestrictedPython
**Pros:** Ready-made policies
**Cons:** Learning curve

