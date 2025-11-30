class Action:
    def __init__(self, app):
        self._app = app

    def do(self):
        raise NotImplementedError(f"{self.__class__.__name__}: do")

    def undo(self):
        raise NotImplementedError(f"{self.__class__.__name__}: undo")

class Insert(Action):
    def __init__(self, app, pos, char):
        super().__init__(app)
        self._pos = pos
        self._char = char

    def do(self):
        self._app._buffer.insert(self._pos, self._char)

    def undo(self):
        self._app._buffer.delete(self._pos)

class Delete(Action):
    def __init__(self, app, pos):
        super().__init__(app)
        self._pos = pos
        self._char = self._app._buffer.char(pos)

    def do(self):
        self._app._buffer.delete(self._pos)

    def undo(self):
        self._app._buffer.insert(self._pos, self._char)

class Move(Action):
    def __init__(self, app, direction):
        super().__init__(app)
        self._direction = direction
        self._old = self._app._cursor.pos()
        self._new = None

    def do(self):
        self._app._cursor.act(self._direction)
        self._new = self._app._cursor.pos()

    def undo(self):
        self._app._cursor.move_to(self._old)

def _interact(self):
    family, key = self._get_key()
    name = f"_do_{family}" if family else f"_do_{key}"
    if not hasattr(self, name):
        return
    action = getattr(self, name)(key)
    self._history.append(action)
    action.do()
    self._add_log(key)

def _do_DELETE(self, key):
    return Delete(self, self._cursor.pos())

def _do_INSERT(self, key):
    return Insert(self, self._cursor.pos(), key)

def _do_KEY_UP(self, key):
    return Move(self, "up")
