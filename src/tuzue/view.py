# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
"""
A View object has the state of a particular view. It's not
necessarily the current view, but it can be so by using the Screen
instance.
"""


class View:
    def __init__(self):
        self.items = {}
        self.item_current = 0
        self.input_string = ""
        self.input_pos = 0

    def set_items(self, items):
        self.items = items

    def visible_items(self):
        for i, item in enumerate(self.items):
            yield item

    def key_down(self):
        if self.item_current < len(self.items) - 1:
            self.item_current += 1

    def key_up(self):
        if self.item_current > 0:
            self.item_current -= 1

    def key_backspace(self):
        if self.input_string:
            self.input_string = self.input_string[:-1]
            self.input_pos -= 1

    def typed(self, char):
        self.input_string += char
        self.input_pos += 1
