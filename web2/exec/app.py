from flask import Flask, request, abort
import ast

app = Flask(__name__)

@app.route('/exec', methods=['POST'])
def run_code():
    code = request.form.get('code', '')
    try:
        # Parse as an expression only
        tree = ast.parse(code, mode='eval')
        # Disallow all builtins
        safe_globals = {'__builtins__': {}}
        result = eval(compile(tree, '<string>', 'eval'), safe_globals, {})
        return str(result), 200
    except Exception:
        abort(400, description='Invalid or unsafe code')

if __name__ == '__main__':
    app.run()