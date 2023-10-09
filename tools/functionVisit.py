import ast

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.current_function = None
        self.function_deps = {}

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.function_deps[self.current_function] = set()
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if self.current_function:
                self.function_deps[self.current_function].add(node.func.id)
        self.generic_visit(node)

def create_dependency_tree(source_code):
    tree = ast.parse(source_code)
    visitor = FunctionVisitor()
    visitor.visit(tree)
    return visitor.function_deps

# Test with some code
code = """
# this is comment of a
def a():
    if 1 == 1:
        c()
    b()
    b()

def b():
    c()

def c():
    print('nothing to call')
"""

print(create_dependency_tree(code))
