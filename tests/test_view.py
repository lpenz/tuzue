# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import tuzue.view

import unittest


class TestView(unittest.TestCase):
    def test_empty(self):
        view = tuzue.view.View(items=[])
        self.assertEqual(list(view.screen_items()), [])
        self.assertEqual(view.selected_item(), None)

    def test_generator(self):
        itemlist = [str(i) for i in range(0, 20)]
        generator = (i for i in itemlist)
        view = tuzue.view.View(generator=generator)
        view.items_generate_all()
        self.assertEqual(list(view.screen_items()), itemlist)
        view.items_update()
        self.assertEqual(list(view.screen_items()), itemlist)

    def test_filtered(self):
        itemlist = [str(i) for i in range(0, 20)]
        view = tuzue.view.View(items=itemlist)
        self.assertEqual(view.selected_item(), "0")
        view.typed("1")
        self.assertEqual(
            list(view.screen_items()),
            ["1"] + ["1%d" % i for i in range(0, 10)],
        )
        self.assertEqual(view.selected_item(), "1")
        view.key_up()
        self.assertEqual(view.selected_item(), "1")
        view.key_down()
        self.assertEqual(view.selected_item(), "10")
        view.typed("0")
        self.assertEqual(view.selected_item(), "10")
        view.key_backspace()
        self.assertEqual(view.selected_item(), "10")
        view.key_up()
        self.assertEqual(view.selected_item(), "1")
        view.typed("z")
        self.assertEqual(list(view.screen_items()), [])
        self.assertEqual(view.selected_item(), None)

    def test_screen(self):
        itemlist = [str(i) for i in range(0, 20)]
        view = tuzue.view.View(items=itemlist)
        view.screen_height_set(3)
        self.assertEqual(list(view.screen_items()), ["0", "1", "2"])
        for i in range(0, 3):
            self.assertEqual(view.screen_selected_line(), i)
            self.assertEqual(view.selected_idx, i)
            self.assertEqual(view.selected_item(), str(i))
            view.key_down()
