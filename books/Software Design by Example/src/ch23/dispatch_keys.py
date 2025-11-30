TRANSLATE = {
    "\x18": "CONTROL_X"
}

def _interact(self):
    key = self._screen.getkey()
    key = self.TRANSLATE.get(key, key)
    name = f"_do_{key}"
    if hasattr(self, name): # 'hasattr' gets all kinds of attributes (including methods)
        getattr(self, name)()

def _do_CONTROL_X(self):
    self._running = False

def _do_KEY_UP(self):
    self._cursor.up()

class DispatchApp(MainApp):
    def __init__(self, size, lines):
        super().__init__(size, lines)
        self._running = True

    def _run(self):
        while self._running:
            self._window.draw(self._lines)
            self._screen.move(*self._cursor.pos())
            self._interact()
