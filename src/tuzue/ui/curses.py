# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
"""
UiCurses class that represents the full state of the curses screen
itself and is able to sync it with the provided view.

Should be instantiated as a singleton.

This class is used to display a particular View instance, and allows
us to have several views on the stack and switch between then
efficiently. It's also a bridge between the View class and the
downstream ui implementation, even though for now only curses is
available.
"""


from contextlib import contextmanager
import curses


class UiCurses:
    """Singleton that controls what is present in the ui"""

    def __init__(self):
        self.stdscr = None

    def start(self):
        """
        Based on
        https://github.com/enthought/Python-2.7.3/blob/master/Lib/curses/wrapper.py
        """
        # Initialize curses
        self.stdscr = curses.initscr()
        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()
        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        self.stdscr.keypad(True)
        # Start color, too.  Harmless if the terminal doesn't have
        # color; user can test with has_color() later on.  The try/catch
        # works around a minor bit of over-conscientiousness in the curses
        # module -- the error return from C start_color() is ignorable.
        try:
            curses.start_color()
            # Reset colors to default
            curses.use_default_colors()
        except Exception:
            pass
        self.winhelp = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
        self.winhelp.addstr(0, 0, "help here")
        self.winhelp.refresh()
        self.prompt = "> "
        self.winprompt = curses.newwin(1, curses.COLS, 0, 0)
        self.winprompt.keypad(True)
        self.winprompt_y = 0
        self.winmenu = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
        self.wins = [self.winhelp, self.winprompt, self.winmenu]
        # self.winmenu = curses.newpad(curses.LINES-2, curses.COLS)

    def end(self):
        if not self.stdscr:
            return
        # Set everything back to normal
        if curses.has_colors():
            curses.use_default_colors()
        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def max_items(self):
        return curses.LINES - 2

    def show(self, view):
        self.winmenu.erase()
        for i, item in enumerate(view.visible_items(self.max_items())):
            self.winmenu.addstr(i, 0, item)
        if view.line is not None:
            self.winmenu.addstr(view.line, 0, view.item, curses.A_REVERSE)
        self.winmenu.noutrefresh()
        self.winprompt.erase()
        self.winprompt.addstr(0, 0, self.prompt)
        self.winprompt.addstr(0, len(self.prompt), view.input.string)
        self.winprompt.noutrefresh()
        curses.setsyx(self.winprompt_y, len(self.prompt) + view.input.pos)
        curses.doupdate()

    def interact(self, view):
        key = self.winprompt.getch()
        if key in {curses.KEY_ENTER, 10, 13}:
            # We are done
            return True
        # Check if it's an edit
        edit_actions = {
            curses.KEY_DOWN: view.key_down,
            curses.KEY_UP: view.key_up,
            curses.KEY_BACKSPACE: view.key_backspace,
        }
        action = edit_actions.get(key)
        if action:
            action()
        else:
            # Check if it's a regular typed char:
            char = chr(key)
            if char.isprintable():
                view.typed(char)
        return False


@contextmanager
def context():
    ui = UiCurses()
    try:
        ui.start()
        yield ui
    finally:
        ui.end()


def main():
    with context() as ui:
        items = [str(i) * 10 for i in range(0, ui.max_items())]
        ui.set("> ", items)
        ui.refresh()
        ui.getkey()


if __name__ == "__main__":
    main()
