def act(self, direction):
    assert hasattr(self, direction)
    getattr(self, direction)()

def move_to(self, pos):
    self._pos = pos
    self._fix()
