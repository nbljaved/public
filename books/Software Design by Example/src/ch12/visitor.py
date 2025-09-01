class Visitor:
    def __init__(self, root):
        self.root = root
        # Here a node will be a BeautifulSoup node

    def walk(self, node=None):
        if node is None:
            node = self.root

        opened = self.open(node)
        # The 'open' method apart from its return value
        # also has 'side-effects', i.e it opens the node
        if opened:
            for child in node.children:
                self.walk(child)

        self.close(node)

    def open(self, node):
        raise NotImplementedError("open")

    def close(self, node):
        raise NotImplementedError("close")
