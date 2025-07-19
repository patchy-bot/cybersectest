# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed use of exec on user input. Introduced safe_eval that parses input with ast, allows only arithmetic nodes. This prevents arbitrary code execution.

## Security Notes
Ensure only whitelisted operations. If new operations needed, explicitly add to SAFE_NODES.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

# Define a safe list of AST node types (only arithmetic)
SAFE_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp,
              ast.Num, ast.Add, ast.Sub, ast.Mult, ast.Div,
              ast.Pow, ast.Mod, ast.UAdd, ast.USub, ast.Load)


def safe_eval(expr: str) -> float:
    """Safely evaluate a mathematical expression with AST."""
    try:
        # Parse the expression to an AST
        node = ast.parse(expr, mode='eval')
        # Recursively validate node types
        for sub in ast.walk(node):
            if not isinstance(sub, SAFE_NODES):
                raise ValueError(f"Disallowed expression: {sub}")
        # Compile and evaluate
        compiled = compile(node, '<string>', 'eval')
        return eval(compiled, {'__builtins__': {}})
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json(force=True)
    expr = data.get('expression', '')
    try:
        result = safe_eval(expr)
        return jsonify({'result': result})
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

if __name__ == '__main__':
    app.run(debug=False)

```

## Additional Dependencies
- ast

## Testing Recommendations
- Test with valid arithmetic expressions
- Test attempts to inject code (e.g. __import__(...) ) and expect rejection

## Alternative Solutions

### Use an existing sandboxed expression evaluator library (e.g. mathjs via API)
**Pros:** Maintenance offloaded to library, Potentially more features
**Cons:** External dependency, May require additional setup

