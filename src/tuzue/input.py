# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
"""
An Input object has the state of the input line
"""


class Input:
    def __init__(self):
        self.string = ""
        self.pos = 0

    def key_backspace(self):
        if self.string:
            self.string = self.string[:-1]
            self.pos -= 1

    def typed(self, char):
        self.string += char
        self.pos += 1
