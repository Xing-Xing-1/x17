import ast

# with open("ok.py", "r") as f:
#    t = f.read()



code = """
# sample.py

# This is a top-level comment

def add(x: int, y: int = 0) -> int:
    \"""Add two numbers together.\"""
    # Inline comment inside function
    result = x + y
    return result

def no_args_func():
    \"""Function with no arguments.\"""
    print("Hello, World!")

def complex_func(a, b=2, *args, c, d=5, **kwargs):
    \"""
    Function with various types of arguments.
    \"""
    pass
"""
# t = """
y = ast.parse(code)


for x in ast.walk(y):
    if isinstance(x, ast.FunctionDef):
        print(x.name)
        
        print(x.__dict__)
        
        print(ast.get_docstring(x))
        print(ast.unparse(x))
        print("===")
        
    
            
