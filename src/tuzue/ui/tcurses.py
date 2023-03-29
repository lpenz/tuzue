# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
"""
UiCurses class that represents the full state of the curses screen
itself and is able to sync it with the provided view.

Should be instantiated as a singleton.

This class is used to display a particular View instance, and allows
us to have several views on the stack and switch between then
efficiently. It serves as a bridge between the View class and the
downstream ui implementation - but for now only curses is available.
"""


import curses
from contextlib import contextmanager
from typing import Callable, Dict, Generator, Iterator, Optional

from tuzue.logger import logger
from tuzue.view import View


class CursesError(Exception):
    pass


class CursesWin:
    """Class that encapsulates a curses window"""

    def __init__(
        self, label: str, height: int, width: int, line: int, col: int
    ) -> None:
        self.height = height
        self.width = width
        self.line = line
        self.col = col
        self.label = label
        self.win = curses.newwin(height, width, line, col)

    def erase(self) -> None:
        self.win.erase()

    def noutrefresh(self) -> None:
        self.win.noutrefresh()

    def addstr(self, line: int, col: int, string: str, *args: int) -> None:
        available = self.width - col
        if len(string) > available:
            string = string[0 : (self.width - col - 4)] + "..."
        try:
            self.win.addstr(line, col, string, *args)
        except curses.error:
            raise CursesError("win {} could not addstr {}\n".format(self.label, string))

    def set_cursor(self, line: int, col: int) -> None:
        curses.setsyx(self.line + line, self.col + col)


@contextmanager
def winfocus(win: CursesWin) -> Generator[CursesWin, None, None]:
    """Window context - makes the code more ergonomic and
    schedules an update upon exit"""
    try:
        yield win
    finally:
        win.noutrefresh()


class Windows:
    """The standard collection of windows we use, for ergonomy"""

    def __init__(
        self, title: CursesWin, prompt: CursesWin, binput: CursesWin, menu: CursesWin
    ) -> None:
        self.title = title
        self.prompt = prompt
        self.binput = binput
        self.menu = menu


class UiCursesBase:
    """
    Base classe for the curses UI that provides the functionality but not the layout.

    Derived classes should def layout(self), override the prompt, etc.
    They can also def input_process to provide additional bindings.
    """

    prompt = "> "
    edit_actions: Dict[bytes, Callable[[View, int, bytes], bool]] = {}
    edit_actions_default = {
        b"KEY_ENTER": View.key_enter,
        b"KEY_DOWN": View.key_down,
        b"KEY_UP": View.key_up,
        b"KEY_PPAGE": View.key_pgup,
        b"KEY_NPAGE": View.key_pgdown,
        b"KEY_HOME": View.key_home,
        b"KEY_END": View.key_end,
        b"KEY_BACKSPACE": View.key_backspace,
        b"KEY_DC": View.key_delete,
        b"KEY_LEFT": View.key_left,
        b"KEY_RIGHT": View.key_right,
        b"^A": View.key_bol,
        b"^E": View.key_eol,
        b"^U": View.key_killbol,
        b"^K": View.key_killeol,
        b"^[KEY_BACKSPACE": View.key_killwordleft,
    }

    def __init__(self) -> None:
        self.stdscr: Optional[curses._CursesWindow] = None
        self.win: Optional[Windows] = None

    def start(self) -> None:
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
        except curses.error:
            pass
        self.layout()

    def end(self) -> None:
        if not self.stdscr:
            return
        # Set everything back to normal
        if curses.has_colors():
            curses.use_default_colors()
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def layout(self) -> None:
        raise NotImplementedError

    def max_items(self) -> int:
        if not self.win:
            return 0
        return self.win.menu.height

    def show(self, view: View) -> None:
        if not self.win:
            return
        # Update menu:
        with winfocus(self.win.menu) as win:
            win.erase()
            max_items = self.max_items()
            if max_items:
                view.screen_height_set(max_items)
            for i, item in enumerate(view.screen_items()):
                win.addstr(i, 0, item)
            if view.screen_selected_line() is not None:
                win.addstr(
                    view.screen_selected_line() or 0,
                    0,
                    view.selected_item() or "",
                    curses.A_REVERSE,
                )
        # Update input:
        with winfocus(self.win.binput) as win:
            win.erase()
            win.addstr(0, 0, view.binput.string)
        # Update title, with status:
        with winfocus(self.win.title) as win:
            win.erase()
            win.addstr(0, 0, view.title)
            status = "%s/%d" % (
                str(
                    view.selected_idx + 1
                    if view.selected_idx is not None
                    else view.selected_idx
                ),
                len(view.items),
            )
            win.addstr(0, win.width - len(status) - 1, status)
        # Position cursor in prompt:
        self.win.prompt.set_cursor(0, len(self.prompt) + view.binput.pos)
        # Refresh screen:
        curses.doupdate()

    def input_read(self, nodelay: bool) -> Optional[tuple[int, bytes]]:
        if not self.win:
            return None
        self.win.binput.win.nodelay(nodelay)
        key = self.win.binput.win.getch()
        if key == -1:
            return key, b""
        if key in {curses.KEY_ENTER, 10, 13}:
            return curses.KEY_ENTER, b"KEY_ENTER"
        if key == 127:
            return curses.KEY_BACKSPACE, b"KEY_BACKSPACE"
        keyname = curses.keyname(key)
        if key == 27:  # ESC
            self.win.binput.win.nodelay(True)
            k = self.win.binput.win.getch()
            if k != -1:
                keyname += curses.keyname(k)
        logger.debug(f"key {key} name {keyname!r}")
        return key, keyname

    def interact(self, view: View) -> bool:
        # Generate first item:
        view.item_generate()
        # Set nonblocking if we have more items to generate, otherwise
        # set blocking mode:
        key_keyname = self.input_read(bool(view.item_generator))
        if not key_keyname:
            return False
        key, keyname = key_keyname
        return self.input_process(view, key, keyname)

    def input_process(self, view: View, key: int, keyname: bytes) -> bool:
        if key == -1:
            return False
        # Check if it's a custom edit_action
        action = self.edit_actions.get(keyname)
        if action:
            return action(view, key, keyname)
        # Check if it's a default edit_action
        action = self.edit_actions_default.get(keyname)
        if action:
            return action(view, key, keyname)
        # Otherwise, check if it's a regular typed char:
        char = None
        try:
            char = chr(key)
        except ValueError:
            pass
        if char and char.isprintable():
            view.typed(char)
        return False


class UiCursesSimple(UiCursesBase):
    """
    Provides the following layout:

    title----------------------------
    prompt- input--------------------
    menu-----------------------------
    |||||||||||||||||||||||||||||||||
    |||||||||||||||||||||||||||||||||
    """

    def layout(self) -> None:
        lines = curses.LINES
        cols = curses.COLS
        title = CursesWin("title", 1, cols, 0, 0)
        with winfocus(CursesWin("prompt", 1, len(self.prompt) + 1, 1, 0)) as win:
            win.addstr(0, 0, self.prompt)
            prompt = win
        inputwidth = cols - len(self.prompt)
        with winfocus(CursesWin("input", 1, inputwidth, 1, len(self.prompt))) as win:
            win.win.keypad(True)
            binput = win
        menulines = lines - 2
        menu = CursesWin("menu", menulines, cols, 2, 0)
        self.win = Windows(title, prompt, binput, menu)


@contextmanager
def context() -> Iterator[UiCursesSimple]:
    ui = UiCursesSimple()
    try:
        ui.start()
        yield ui
    finally:
        ui.end()
