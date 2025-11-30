def main(stdscr, lines):
    while True:
        stdscr.erase() # erase the screen
        for (y, line) in enumerate(lines):
            stdscr.addstr(y, 0, line)
        key = stdscr.getkey()
        if key.lower() == "q":
            return

if __name__ == "__main__":
    num_lines, logfile = int(sys.argv[1]), sys.argv[2]
    lines = make_lines(num_lines)
    open_log(logfile)
    curses.wrapper(lambda stdscr: main(stdscr, lines))

from string import ascii_lowercase

def make_lines(num_lines):
    result = []
    for i in range(num_lines):
        ch = ascii_lowercase[i % len(ascii_lowercase)]
        result.append(ch + "".join(str(j % 10) for j in range(i)))
    return result
