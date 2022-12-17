import curses
from typing import Generator
import sys

from pyfiglet import Figlet
import time


def _wait(s: int) -> Generator:
    for i in range(s - 1, -1, -1):
        yield i
        time.sleep(1)


def _convert2second(hhmm: str) -> int:
    hour, _, minute = hhmm.partition(":")
    return int(hour) * 3600 + int(minute) * 60


def get_user_entry(stdscr):
    entry_done = False
    timeout = ""
    while True:
        if entry_done:
            if timeout == "q":
                return -1
            try:
                timeout_s = _convert2second(timeout)
                break
            except ValueError:
                timeout = ""
                entry_done = False

        else:
            stdscr.addstr(0, 0, "Enter time as hh:mm to count down or q to quit: ")
            stdscr.clrtoeol()
            stdscr.addstr(timeout)

            char = stdscr.get_wch()
            if isinstance(char, str) and char.isprintable():
                timeout += char
            elif char == curses.KEY_BACKSPACE:
                timeout = timeout[:-1]
            elif char == "\n":
                entry_done = True
    return timeout_s


def c_main(
    stdscr: "curses._CursesWindow",
) -> int:
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    f = Figlet(font="roman___")
    timeout_s = get_user_entry(stdscr)
    if timeout_s == -1:
        return 0

    for i in _wait(timeout_s):
        stdscr.clear()
        text_to_render = f"{i//3600:02d} : {((i%3600) // 60):02d} : {i%60:02d}"
        stdscr.addstr(f.renderText(text_to_render))
        stdscr.refresh()
        stdscr.nodelay(True)
        try:
            c = stdscr.get_wch()
            if c == "q":
                break
        except curses.error:
            pass
    stdscr.nodelay(False)
    _ = stdscr.get_wch()
    return 0


def main(argv=sys.argv) -> int:
    return curses.wrapper(c_main)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
