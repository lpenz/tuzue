# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import tuzue.view

import unittest


class TestView(unittest.TestCase):
    def setUp(self):
        self.view = tuzue.view.View()

    def test_empty(self):
        self.view.items_set([])
        self.assertEqual(list(self.view.visible_items(999)), [])
        self.assertEqual(self.view.selected_item(), None)

    def test_visible(self):
        items = [str(i) for i in range(0, 20)]
        self.view.items_set(items)
        self.assertEqual(list(self.view.visible_items(999)), items)
        self.assertEqual(self.view.selected_item(), "0")
        self.view.typed("2")
        self.assertEqual(list(self.view.visible_items(999)), ["2", "12"])
        self.assertEqual(self.view.selected_item(), "2")
