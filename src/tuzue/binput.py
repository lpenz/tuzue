# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
"""
A Binput object has the state of the input line
"""


class Binput:
    def __init__(self, string: str = ""):
        self.string = string
        self.pos = len(string)

    def typed(self, char: str) -> None:
        self.string = self.string[: self.pos] + char + self.string[self.pos :]
        self.pos += 1

    def key_backspace(self) -> None:
        if self.string and self.pos > 0:
            self.string = self.string[: self.pos - 1] + self.string[self.pos :]
            self.pos -= 1

    def key_delete(self) -> None:
        if self.string and self.pos < len(self.string):
            self.string = self.string[: self.pos] + self.string[self.pos + 1 :]

    def key_left(self) -> None:
        if self.string and self.pos > 0:
            self.pos -= 1

    def key_right(self) -> None:
        if self.pos < len(self.string):
            self.pos += 1

    def key_bol(self) -> None:
        self.pos = 0

    def key_eol(self) -> None:
        self.pos = len(self.string)

    def key_killbol(self) -> None:
        self.string = self.string[self.pos :]
        self.pos = 0

    def key_killeol(self) -> None:
        self.string = self.string[: self.pos]

    def key_killwordleft(self) -> None:
        if self.pos == 0:
            return
        start = self.pos - 1
        while self.string[start].isspace() and start > 0:
            start -= 1
        while not self.string[start].isspace() and start > 0:
            start -= 1
        if start == 0:
            self.string = ""
            self.pos = 0
            return
        start += 1
        left = self.string[0:start]
        right = self.string[self.pos :]
        self.string = left + right
        self.pos = start
