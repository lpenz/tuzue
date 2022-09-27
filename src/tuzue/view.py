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
        # All items:
        self.items_all = []
        # Items filtered by input:
        self.items_filtered = []
        # Selected item, identified by items_filtered index:
        self.selected_idx = 0
        # Generator, when in use:
        self.generator = None
        # Self-managed input object:
        self.input = tuzue.input.Input()
        # Path, shown in header:
        self.path = ""
        self.reset()

    def reset(self):
        self.items_all = []
        self.items_filtered = []
        self.selected_idx = None

    def selected_item(self):
        if self.selected_idx is not None:
            return self.items_filtered[self.selected_idx]
        return None

    def items_set(self, items):
        """Sets (overrides) the whole items list"""
        self.reset()
        self.items_all = items
        self.items_filtered_update()

    def item_generator_set(self, generator):
        """Sets the item generator and resets the internal states as necessary"""
        self.reset()
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
            wasempty = self.items_filtered == []
            item = next(self.generator)
            self.items_all.append(item)
            if self.item_filter(item):
                self.items_filtered.append(item)
                if self.selected_idx is None and wasempty:
                    self.selected_idx = 0
            return True
        except StopIteration:
            self.generator = None
            return False

    def item_filter(self, item):
        """Returns True if the provided item should be shown, given the current input"""
        return not self.input.string or self.input.string in item

    def items_filtered_update(self):
        """Resets and updates the whole items_filtered list using the current input;
        also resets the selected_idx if necessary"""
        selected_item = None
        if self.selected_idx is not None:
            selected_item = self.items_filtered[self.selected_idx]
        self.items_filtered = []
        self.selected_idx = None
        idx = 0
        for item in self.items_all:
            if self.item_filter(item):
                self.items_filtered.append(item)
                if item == selected_item:
                    self.selected_idx = idx
                idx += 1
        if self.selected_idx is None and self.items_filtered:
            self.selected_idx = 0

    def visible_items(self, max_items):
        line = 0
        for idx, item in enumerate(self.items_filtered):
            if line >= max_items:
                break
            yield item
            line += 1

    def selected_line(self):
        return self.selected_idx

    def move_to_idx(self, idx):
        if idx < 0 or idx >= len(self.items_filtered):
            return
        self.selected_idx = idx

    def key_down(self):
        self.move_to_idx(self.selected_idx + 1)

    def key_up(self):
        self.move_to_idx(self.selected_idx - 1)

    def key_backspace(self):
        self.input.key_backspace()
        self.items_filtered_update()

    def typed(self, char):
        self.input.typed(char)
        self.items_filtered_update()
