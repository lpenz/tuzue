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
    def __init__(self, items=None, generator=None):
        # One of the mutually-exclusive arguments must be provided:
        assert (items is None) != (generator is None)
        # All items:
        self.items_all = items or []
        # item_generator, when in use:
        self.item_generator = generator
        # Effective items, filtered by input:
        self.items = []
        # Selected item, identified by items index:
        self.selected_idx = None
        # Screen-related members:
        self.screen_height = None
        # Self-managed input object:
        self.input = tuzue.input.Input()
        # Path, shown in header:
        self.path = ""
        # Reset to sync selected_idx with items:
        self.reset()

    def reset(self):
        """
        Reset self.items to self.items_all, as if we had no filter input.
        Reset selected_idx.
        """
        self.items = list(self.items_all) or []
        self.selected_idx = 0 if self.items else None

    # Item generation methods:

    def item_generate(self):
        """
        Generate one item using self.item_generator, if possible, and append it to
        self.items_all.

        Returns True if an item was generated, or False otherwise - if we are already
        done, for instance.
        """
        if not self.item_generator:
            return False
        try:
            wasempty = self.items == []
            item = next(self.item_generator)
            self.items_all.append(item)
            if self.item_filter(item):
                self.items.append(item)
                if self.selected_idx is None and wasempty:
                    self.selected_idx = 0
            return True
        except StopIteration:
            self.item_generator = None
            return False

    def items_generate_all(self):
        while self.item_generate():
            pass

    # Item filtering methods:

    def item_filter(self, item):
        """Returns True if the provided item should be shown, given the current input"""
        return not self.input.string or self.input.string in item

    def items_update(self):
        """Resets and updates the whole self.items list using the current input;
        also resets selected_idx if necessary"""
        selected_item = None
        if self.selected_idx is not None:
            selected_item = self.items[self.selected_idx]
        self.items = []
        self.selected_idx = None
        idx = 0
        for item in self.items_all:
            if self.item_filter(item):
                self.items.append(item)
                if item == selected_item:
                    self.selected_idx = idx
                idx += 1
        if self.selected_idx is None and self.items:
            self.selected_idx = 0

    # Selected idx/items methods:

    def selected_idx_set(self, idx):
        if idx < 0 or idx >= len(self.items):
            return
        self.selected_idx = idx

    def selected_item(self):
        if self.selected_idx is not None:
            return self.items[self.selected_idx]
        return None

    # Screen methods, used to generate the concrete view:

    def screen_height_set(self, height):
        old_screen_height = self.screen_height
        self.screen_height = height
        if height != old_screen_height:
            self.reset()

    def screen_items(self):
        line = 0
        for idx, item in enumerate(self.items):
            if self.screen_height is not None and line >= self.screen_height:
                break
            yield item
            line += 1

    def screen_selected_line(self):
        return self.selected_idx

    # Key reactors:

    def key_down(self):
        self.selected_idx_set(self.selected_idx + 1)

    def key_up(self):
        self.selected_idx_set(self.selected_idx - 1)

    def key_backspace(self):
        self.input.key_backspace()
        self.items_update()

    def typed(self, char):
        self.input.typed(char)
        self.items_update()
