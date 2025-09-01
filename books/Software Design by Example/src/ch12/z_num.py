def open(expander, node):
    expander.showTag(node, closing=False)
    expander.output(node.attrs["z-num"])

def close(expander, node):
    expander.showTag(node, closing=True)
