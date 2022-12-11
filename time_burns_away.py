import curses
from typing import Generator
import sys

from pyfiglet import Figlet


def _wait(s: int) -> Generator:
    import time

    for i in range(s - 1, -1, -1):
        time.sleep(1)
        yield i


def _convert2second(hhmm: str) -> int:
    hour, _, minute = hhmm.partition(":")
    return int(hour) * 3600 + int(minute) * 60


def c_main(
    stdscr: "curses._CursesWindow",
) -> int:
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    f = Figlet(font="roman___")
    entry_done = False
    timeout = ""
    while True:
        if entry_done:
            try:
                timeout_s = _convert2second(timeout)
                break
            except ValueError:
                timeout = ""
                entry_done = False

        else:
            stdscr.addstr(0, 0, "Enter time as hh:mm to count down: ")
            stdscr.clrtoeol()
            stdscr.addstr(timeout)

            char = stdscr.get_wch()
            if isinstance(char, str) and char.isprintable():
                timeout += char
            elif char == curses.KEY_BACKSPACE:
                timeout = timeout[:-1]
            elif char == "\n":
                entry_done = True

    tmp = f"{timeout_s//3600:02d} : {((timeout_s%3600) // 60):02d} : {timeout_s%60:02d}"
    text_to_render = tmp

    stdscr.attron(curses.color_pair(1))
    stdscr.clear()
    stdscr.addstr(
        0,
        0,
        f.renderText(text_to_render),
    )
    stdscr.refresh()
    for i in _wait(timeout_s):
        if not i == timeout_s:
            stdscr.clear()
            text_to_render = f"{i//3600:02d} : {((i%3600) // 60):02d} : {i%60:02d}"
            stdscr.addstr(f.renderText(text_to_render))
            stdscr.refresh()
    char = stdscr.get_wch()
    return 0


def main(argv=sys.argv) -> int:
    return curses.wrapper(c_main)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
