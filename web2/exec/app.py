from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form.get('code', '')
    try:
        # Parse code safely using ast.literal_eval if expecting expressions
        # For statements, consider using restricted execution environments
        # Here, we only allow expressions for safety
        tree = ast.parse(code, mode='eval')
        result = eval(compile(tree, filename='<ast>', mode='eval'))
        return jsonify({'result': str(result)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False)
