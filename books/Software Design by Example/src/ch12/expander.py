from env import Env
from visitor import Visitor
from bs4 import NavigableString

import z_if
import z_loop
import z_num
import z_var

HANDLERS = {
    "z-if": z_if,
    "z-loop": z_loop,
    "z-num": z_num,
    "z-var": z_var
}


class Expander(Visitor):
    def __init__(self, root, variables):
        super().__init__(root)
        self.env = Env(variables) # variables is a dict of variable: value
        self.handlers = HANDLERS # dict of special_attribute: special_object_object
        self.result = []

    def open(self, node):
        if isinstance(node, NavigableString):
            self.output(node.string)
            return False
        elif self.hasHandler(node):
            # The handler is supposed to handle itself
            # as-well-as open the node it is in.
            return self.getHandler(node).open(self, node)
        else:
            self.showTag(node, closing=False)
            # showTag handles a normal html node's opening/closing
            return True
    
    def close(self, node):
        if isinstance(node, NavigableString):
            pass
        elif self.hasHandler(node):
            # The handler is supposed to handle itself
            # as-well-as close the node it is in.
            return self.getHandler(node).close(self, node)
        else:
            self.showTag(node, closing=True)
            # showTag handles a normal html node's opening/closing
            return True
    
    def hasHandler(self, node):
        return any(
            name in self.handlers
            for name in node.attrs
        )
    
    def getHandler(self, node):
        possible = [
            name for name in node.attrs
            if name in self.handlers
        ]
        assert len(possible) == 1, "Should be exactly one handler"
        return self.handlers[possible[0]]
    
    def showTag(self, node, closing):
        if closing:
            self.output(f"</{node.name}>")
            return
        self.output(f"<{node.name}")
    
        # If opening:
        for name in node.attrs:
            # showTag is also used by the handler functions themselves
            # therefore we must remove any attributes that start with 'z-'
            if not name.startswith("z-"):
                self.output(f' {name}="{node.attrs[name]}"')
        self.output(">")
    
    def output(self, text):
        # Doesn't output to stdout !!
        self.result.append("UNDEF" if text is None else text)
    
    def getResult(self):
        return "".join(self.result)
