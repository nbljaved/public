class Window:
    def __init__(self, screen):
        self._screen = screen

    def draw(self, lines):
        self._screen.erase()
        for (y, line) in enumerate(lines):
            if 0 <= y < curses.LINES: # limit rows shows
                self._screen.addstr(y, 0, line[:curses.COLS]) # limit columns shown

def main(stdscr, lines):
    window = Window(stdscr)
    window.draw(lines)
    while True:
        key = stdscr.getkey()
        if key.lower() == "q":
            return
