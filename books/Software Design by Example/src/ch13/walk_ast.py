import ast
import sys

class CollectNames(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.names = {} # this is a dict (NOT a set !)

    def visit_Assign(self, node):
        # see 'targets' in 'Assign' of our ast dump of the previous example
        for var in node.targets:
            self.add(var, var.id)
        self.generic_visit(node) # generic_visit is a NodeVisitor method

    def visit_FunctionDef(self, node):
        self.add(node, node.name)
        self.generic_visit(node)

    def add(self, node, name):
        loc = (node.lineno, node.col_offset)
        self.names[name] = self.names.get(name, set())
        self.names[name].add(loc)

    def position(self, node):
        return ({node.lineno}, {node.col_offset})

with open(sys.argv[1], 'r') as reader:
    source = reader.read()
tree = ast.parse(source)
collector = CollectNames()
collector.visit(tree)
print(collector.names)
