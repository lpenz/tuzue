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

# Number of lines non-free lines already allocated to specific
# functions:
LINES_USED = 2


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
        self.winpath = curses.newwin(1, curses.COLS, 0, 0)
        self.winpath.noutrefresh()
        self.prompt = "> "
        self.wininput_y = 1
        self.winprompt = curses.newwin(1, len(self.prompt) + 1, self.wininput_y, 0)
        self.winprompt.addstr(0, 0, self.prompt)
        self.winprompt.noutrefresh()
        self.wininput = curses.newwin(
            1, curses.COLS - len(self.prompt), self.wininput_y, len(self.prompt)
        )
        self.wininput.keypad(True)
        self.wininput.noutrefresh()
        self.winmenu = curses.newwin(curses.LINES - LINES_USED, curses.COLS, 2, 0)
        self.winmenu.noutrefresh()
        curses.doupdate()

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
        return curses.LINES - LINES_USED

    def show(self, view):
        # Update menu:
        self.winmenu.erase()
        view.screen_height_set(self.max_items())
        for i, item in enumerate(view.screen_items()):
            self.winmenu.addstr(i, 0, item)
        if view.screen_selected_line() is not None:
            self.winmenu.addstr(
                view.screen_selected_line(), 0, view.selected_item(), curses.A_REVERSE
            )
        self.winmenu.noutrefresh()
        # Update input:
        self.wininput.erase()
        self.wininput.addstr(0, 0, view.input.string)
        self.wininput.noutrefresh()
        # Update path, with status:
        self.winpath.erase()
        self.winpath.addstr(0, 0, view.path)
        status = "%s/%d" % (
            str(
                view.selected_idx + 1
                if view.selected_idx is not None
                else view.selected_idx
            ),
            len(view.items),
        )
        self.winpath.addstr(0, curses.COLS - len(status) - 1, status)
        self.winpath.noutrefresh()
        # Position cursor in prompt:
        curses.setsyx(self.wininput_y, len(self.prompt) + view.input.pos)
        # Refresh screen:
        curses.doupdate()

    def input_read(self):
        key = self.wininput.getch()
        if key == -1:
            return key, None
        keyname = curses.keyname(key)
        if key == 27:
            self.wininput.nodelay(True)
            k = self.wininput.getch()
            if k != -1:
                keyname += curses.keyname(k)
        return key, keyname

    def interact(self, view):
        # Generate first item:
        view.item_generate()
        # Set nonblocking if we have more items to generate, otherwise
        # set blocking mode:
        self.wininput.nodelay(bool(view.item_generator))
        key, keyname = self.input_read()
        if key == -1:
            return False
        if key in {curses.KEY_ENTER, 10, 13}:
            # If the user hit ENTER, we are done
            return True
        # Check if it's an edit
        edit_actions = {
            b"KEY_DOWN": view.key_down,
            b"KEY_UP": view.key_up,
            b"KEY_BACKSPACE": view.key_backspace,
            b"KEY_PPAGE": view.key_pgup,
            b"KEY_NPAGE": view.key_pgdown,
        }
        action = edit_actions.get(keyname)
        if action:
            action()
        else:
            # Check if it's a regular typed char:
            char = None
            try:
                char = chr(key)
            except ValueError:
                pass
            if char and char.isprintable():
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
