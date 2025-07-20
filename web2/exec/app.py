from flask import Flask, request, render_template
import restrictedpython

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    user_code = request.form.get('code', '')
    # Use RestrictedPython to sandbox
    try:
        compiled = restrictedpython.compile_restricted(user_code, '<inline>', 'exec')
        exec_globals = restrictedpython.safe_globals.copy()
        exec(compiled, exec_globals)
        output = exec_globals.get('_print_', '')
    except Exception as e:
        output = f"Error: {e}"
    return render_template('result.html', output=output)

if __name__ == '__main__':
    app.run()