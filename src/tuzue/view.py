# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
"""
A View object has the state of a particular view. It's not
necessarily the current view, but it can be so by using the Screen
instance.
"""

import tuzue.input


class View:
    def __init__(self):
        self.items = []
        self.line = 0
        self.line2idx = {}
        self.selected = None
        self.generator = None
        self.input = tuzue.input.Input()
        self.path = ""

    def items_set(self, items):
        self.items = items
        if self.items:
            self.selected = items[0]

    def item_generator_set(self, generator):
        self.generator = generator

    def item_generate(self):
        """
        Generate one item using self.generator, if possible.

        Returns True if an item was generated, or False otherwise - if we are already
        done, for instance.
        """
        if not self.generator:
            return False
        try:
            wasempty = self.items == []
            self.items.append(next(self.generator))
            if self.selected is None and wasempty:
                self.selected = self.items[0]
            return True
        except StopIteration:
            self.generator = None
            return False

    def visible_items(self, max_items):
        self.line2idx = {}
        line = 0
        self.line = None
        for idx, item in enumerate(self.items):
            if self.input.string not in item:
                continue
            if line >= max_items:
                break
            if item == self.selected:
                # If we'll yield the current item,
                # update current line:
                self.line = line
            self.line2idx[line] = idx
            yield item
            line += 1
        if self.line is None and self.items and self.line2idx:
            # No current line, go to top item:
            self.line = 0
            idx = self.line2idx[self.line]
            self.selected = self.items[idx]
        if not self.line2idx:
            self.selected = None

    def selected_item(self):
        return self.selected

    def move_to_line(self, line):
        if line in self.line2idx:
            self.line = line
        idx = self.line2idx.get(self.line, 0)
        self.selected = self.items[idx]

    def key_down(self):
        self.move_to_line(self.line + 1)

    def key_up(self):
        self.move_to_line(self.line - 1)

    def key_backspace(self):
        self.input.key_backspace()

    def typed(self, char):
        self.input.typed(char)
