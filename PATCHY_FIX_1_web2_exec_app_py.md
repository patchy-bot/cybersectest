# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Replaces exec() with ast.literal_eval() after parsing the expression AST and walking it to block any function calls, attribute access, imports, or other unsafe nodes. This prevents arbitrary code execution.

## Security Notes
By whitelisting only literal nodes and rejecting anything else, we ensure no code injection or RCE. If more complex expressions are needed, implement a safe expression evaluator or restrict allowed operations further.

## Fixed Code
```py
from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/eval', methods=['POST'])
def evaluate():
    data = request.json
    expr = data.get('expr', '')
    try:
        # Only allow safe literal expressions (numbers, strings, tuples, lists, dicts)
        # Disallow any function calls or attribute access
        node = ast.parse(expr, mode='eval')
        for sub in ast.walk(node):
            if isinstance(sub, (ast.Call, ast.Attribute, ast.Import, ast.ImportFrom, ast.Exec, ast.Global, ast.Lambda)):
                raise ValueError('Expression contains unsafe operations')
        result = ast.literal_eval(node)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()

```

## Additional Dependencies
- ast

## Testing Recommendations
- POST valid literal expressions and verify correct results
- POST expressions containing calls or attributes and verify rejection

## Alternative Solutions
None provided
