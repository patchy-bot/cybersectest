import base64
import zlib
import ast

def run_payload(data):
    # Decode and decompress
    compressed = base64.b64decode(data)
    source = zlib.decompress(compressed).decode('utf-8')
    # Parse with AST and allow only expression or limited statements
    tree = ast.parse(source, mode='exec')
    for node in ast.walk(tree):
        # Disallow import, exec, eval, subprocess, os, open
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            raise ValueError("Imports not allowed")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('exec','eval','open', 'compile'):
            raise ValueError("Disallowed function call")
    compiled = compile(tree, '<payload>', 'exec')
    exec(compiled, {'__builtins__': {}}, {})

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: stage_2.py <base64data>")
        sys.exit(1)
    run_payload(sys.argv[1])