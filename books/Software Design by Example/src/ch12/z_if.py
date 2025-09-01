def open(expander, node):
    check = expander.env.find(node.attrs["z-if"])
    if check:
        expander.showTag(node, closing=False)
    return check

def close(expander, node):
    check = expander.env.find(node.attrs["z-if"])
    if check:
        expander.showTag(node, closing=True)
