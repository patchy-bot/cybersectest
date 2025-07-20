from flask import Flask, request, jsonify
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_user_code():
    # Only accept JSON with "code" field
    code = request.json.get('code', '')
    try:
        # Compile the user-provided code in restricted mode
        compiled_code = compile_restricted(code, '<string>', 'exec')
        # Provide only safe builtins
        safe_globals = {
            '__builtins__': safe_builtins
        }
        safe_locals = {}
        # Execute in a sandboxed environment
        exec(compiled_code, safe_globals, safe_locals)
        # Return any variable named 'result' defined by the user code
        output = safe_locals.get('result', None)
        return jsonify({'output': output}), 200
    except Exception as e:
        # Return error without leaking internals
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()