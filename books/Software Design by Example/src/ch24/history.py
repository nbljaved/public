class HistoryApp(InsertDeleteApp):
    def __init__(self, size, keystrokes):
        super().__init__(size, keystrokes)
        self._history = []

    def get_history(self):
        return self._history

    def _do_DELETE(self):
        row, col = self._cursor.pos()
        char = self._buffer.char((row, col))
        self._history.append(("delete", (row, col), char))
        self._buffer.delete(self._cursor.pos())
