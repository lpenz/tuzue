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

    def test_generator(self):
        itemlist = [str(i) for i in range(0, 20)]
        items = (i for i in itemlist)
        self.view.item_generator_set(items)
        self.view.items_generate_all()
        self.view.items_filtered_update()
        self.assertEqual(list(self.view.visible_items(999)), itemlist)

    def test_filtered(self):
        itemlist = [str(i) for i in range(0, 20)]
        self.view.items_set(itemlist)
        self.assertEqual(self.view.selected_item(), "0")
        self.view.typed("1")
        self.assertEqual(
            list(self.view.visible_items(999)),
            ["1"] + ["1%d" % i for i in range(0, 10)],
        )
        self.assertEqual(self.view.selected_item(), "1")
        self.view.key_down()
        self.assertEqual(self.view.selected_item(), "10")
        self.view.typed("0")
        self.assertEqual(self.view.selected_item(), "10")
        self.view.key_backspace()
        self.assertEqual(self.view.selected_item(), "10")
        self.view.key_up()
        self.assertEqual(self.view.selected_item(), "1")
        self.view.typed("z")
        self.assertEqual(list(self.view.visible_items(999)), [])
        self.assertEqual(self.view.selected_item(), None)

    def test_visible(self):
        itemlist = [str(i) for i in range(0, 20)]
        self.view.items_set(itemlist)
        self.assertEqual(list(self.view.visible_items(3)), ["0", "1", "2"])
