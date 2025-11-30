class Buffer:
    def __init__(self, lines):
        self._lines = lines[:]

    def lines(self):
        return self._lines

class BufferApp(DispatchApp):
    def __init__(self, size, lines):
        super().__init__(size, lines)

    def _setup(self, screen):
        self._screen = screen
        # Factory methods !
        self._make_window()
        self._make_buffer()
        self._make_cursor()

    def _make_window(self):
        self._window = Window(self._screen, self._size)

    def _make_buffer(self):
        self._buffer = Buffer(self._lines)

    def _make_cursor(self):
        self._cursor = Cursor()
