# Security Fix for web2/exec/app.py

**Vulnerability Type:** CODE_INJECTION  
**Confidence Level:** HIGH  
**Breaking Changes:** No

## Original Issue
Removed use of Python exec on raw user input. Compiles the code with RestrictedPython which enforces sandbox policies and only exposes a limited builtins set. Also validates that input is a string of reasonable length. The exec now runs in a restricted global scope with safe_builtins.

## Security Notes
Consider further restricting available builtins and monitoring runtime resource usage. Avoid side-effect functions. If full sandboxing is required, run code in a separate container or process with OS-level isolation.

## Fixed Code
```py
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    user_code = request.json.get('code', '')
    if not isinstance(user_code, str) or len(user_code) > 1000:
        return jsonify({'error': 'Invalid code input'}), 400
    # Compile user code with RestrictedPython
    try:
        byte_code = compile_restricted(user_code, '<user_code>', 'exec')
        policy_globals = dict(__builtins__=safe_builtins)
        policy_globals['_print_'] = print  # allow printing
        policy_locals = {}
        exec(byte_code, policy_globals, policy_locals)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': policy_locals.get('result', None)})

if __name__ == '__main__':
    app.run()

```

## Additional Dependencies
- RestrictedPython

## Testing Recommendations
- Submit valid and malicious code snippets to /run endpoint
- Verify that filesystem and OS modules are inaccessible
- Measure performance impact under load

## Alternative Solutions

### Use a microvirtual machine or container to execute code
**Pros:** Strong isolation, Language-agnostic
**Cons:** Higher operational overhead, Slower startup

### Implement a custom AST transformer to whitelist only safe operations
**Pros:** Fine-grained control
**Cons:** Complex to maintain and may miss edge cases

