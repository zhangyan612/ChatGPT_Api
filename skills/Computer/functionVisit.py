import ast

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.current_function = None
        self.function_deps = {filename: {}}
        self.filename = filename

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.function_deps[self.filename][self.current_function] = set()
        self.generic_visit(node)
        self.current_function = None

    def visit_ClassDef(self, node):
        for subnode in node.body:
            if isinstance(subnode, ast.FunctionDef):
                self.visit_FunctionDef(subnode)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == 'self':
            if self.current_function:
                self.function_deps[self.filename][self.current_function].add(node.func.attr)
        self.generic_visit(node)

def create_dependency_tree(source_code, filename):
    tree = ast.parse(source_code)
    visitor = FunctionVisitor(filename)
    visitor.visit(tree)
    return visitor.function_deps

# Test with some code
code = """
class MyClass:
    def method_a(self):
        self.method_b()
        self.method_c()

    def method_b(self):
        self.method_c()

    def method_c(self):
        pass
"""

print(create_dependency_tree(code, 'test.py'))
