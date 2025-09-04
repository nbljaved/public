import ast
from collections import Counter

class FindDuplicateKeys(ast.NodeVisitor):
    def visit_Dict(self, node):
        seen = Counter()
        for key in node.keys:
            if isinstance(key, ast.Constant):
                seen[key.value] += 1
        problems = {k for (k,v) in seen.items() if v > 1}
        self.report(node, problems)
        self.generic_visit(node)

    def report(self, node, problems):
        if problems:
            msg = ', '.join(p for p in problems)
            print(f'duplicates key(s) {{{msg}}} at {node.lineno}')

tree = ast.parse("""
has_duplicates = {
    "third": 3,
    "fourth": 4,
    "fourth": 5,
    "third": 6
}
print(has_duplicates)
""")
duplicates = FindDuplicateKeys()
duplicates.visit(tree)
