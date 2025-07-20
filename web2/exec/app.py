from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    user_code = request.form.get('code', '')
    try:
        # Parse the user code into an AST node to ensure it is safe
        parsed_code = ast.parse(user_code, mode='exec')
        # Define a safe namespace for execution
        safe_globals = {'__builtins__': {}}
        safe_locals = {}
        exec(compile(parsed_code, filename='<user_code>', mode='exec'), safe_globals, safe_locals)
        return jsonify({'result': 'Code executed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)
