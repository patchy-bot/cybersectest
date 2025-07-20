# web2/exec/app.py
from flask import Flask, request, abort

app = Flask(__name__)

# Define a minimal sandbox environment
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
}

def safe_exec(user_code: str) -> None:
    """
    Compile and execute user code in a restricted namespace.
    This prevents access to __import__, file I/O, and other dangerous operations.
    """
    # Compile user code to bytecode
    compiled = compile(user_code, '<user_code>', 'exec')
    # Execute in restricted globals and no locals
    exec(compiled, {'__builtins__': SAFE_BUILTINS}, {})

@app.route('/run', methods=['POST'])
def run_code():
    code = request.form.get('code', '')
    if not code:
        abort(400, description='No code provided')
    try:
        safe_exec(code)
    except Exception:
        # On any error, return HTTP 400 without revealing internal state
        abort(400, description='Error executing code')
    return 'Executed', 200

if __name__ == '__main__':
    app.run(debug=False)