import sys
from visitor import Visitor

class Catalog(Visitor):
    def __init__(self):
        super().__init__()
        self.catalog = {}

    def _tag_enter(self, node):
        if node.name not in self.catalog:
            self.catalog[node.name] = set()
        for child in node:
            if isinstance(child, Tag):
                self.catalog[node.name].add(child.name)

with open(sys.argv[1], "r") as reader:
    text = reader.read()
doc = BeautifulSoup(text, "html.parser")

cataloger = Catalog()
cataloger.visit(doc.html)
result = cataloger.catalog

for tag, contents in sorted(result.items()):
    print(f"{tag}: {', '.join(sorted(contents))}")
