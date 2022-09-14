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
        self.line = 0
        self.line2idx = {}
        self.item = None
        self.input_string = ""
        self.input_pos = 0

    def set_items(self, items):
        self.items = items
        self.item = items[0]

    def visible_items(self, max_items):
        self.line2idx = {}
        line = 0
        self.line = None
        for idx, item in enumerate(self.items):
            if self.input_string not in item:
                continue
            if line >= max_items:
                break
            if item == self.item:
                # If we'll yield the current item,
                # update current line:
                self.line = line
            self.line2idx[line] = idx
            yield item
            line += 1
        if self.line is None:
            # No current line, go to top item:
            self.line = 0
            idx = self.line2idx[self.line]
            self.item = self.items[idx]

    def selected_item(self):
        return self.item

    def move_to_line(self, line):
        if line in self.line2idx:
            self.line = line
        idx = self.line2idx.get(self.line, 0)
        self.item = self.items[idx]

    def key_down(self):
        self.move_to_line(self.line + 1)

    def key_up(self):
        self.move_to_line(self.line - 1)

    def key_backspace(self):
        if self.input_string:
            self.input_string = self.input_string[:-1]
            self.input_pos -= 1

    def typed(self, char):
        self.input_string += char
        self.input_pos += 1
