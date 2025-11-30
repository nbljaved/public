class ClipCursorFixed(ClipCursor):
    def up(self):
        super().up()
        self._fix()

    def down(self):
        super().down()
        self._fix()

    def _fix(self):
        self._pos[COL] = min(
            self._pos[COL],
            (self._buffer.ncol(self._pos[ROW])-1))
