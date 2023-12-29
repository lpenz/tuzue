# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import unittest

import tuzue.view


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

    def test_filter(self):
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
        itemlist = [str(i) for i in range(0, 10)]
        view = tuzue.view.View(items=itemlist)
        view.screen_height_set(3)
        self.assertEqual(list(view.screen_items()), ["0", "1", "2"])
        for i in range(0, 3):
            self.assertEqual(view.selected_idx, i)
            self.assertEqual(view.selected_item(), str(i))
            self.assertEqual(view.screen_selected_line(), i)
            view.key_down()
        for i in range(3, 10):
            self.assertEqual(view.selected_idx, i)
            self.assertEqual(view.selected_item(), str(i))
            self.assertEqual(view.screen_selected_line(), 2)
            view.key_down()
        for i in range(9, 6, -1):
            self.assertEqual(view.selected_idx, i)
            self.assertEqual(view.selected_item(), str(i))
            self.assertEqual(view.screen_selected_line(), i - 7)
            view.key_up()
        for i in range(6, -1, -1):
            self.assertEqual(view.selected_idx, i)
            self.assertEqual(view.selected_item(), str(i))
            self.assertEqual(view.screen_selected_line(), 0)
            view.key_up()
        self.assertEqual(view.selected_idx, 0)
        self.assertEqual(view.selected_item(), "0")
        self.assertEqual(view.screen_selected_line(), 0)

    def test_screen_filter(self):
        itemlist = [str(i) for i in range(0, 20)]
        view = tuzue.view.View(items=itemlist)
        view.screen_height_set(3)
        self.assertEqual(list(view.screen_items()), ["0", "1", "2"])
        self.assertEqual(view.selected_item(), "0")
        view.typed("1")
        self.assertEqual(list(view.screen_items()), ["1", "10", "11"])
        self.assertEqual(view.selected_idx, 0)
        self.assertEqual(view.selected_item(), "1")
        self.assertEqual(view.screen_selected_line(), 0)
        view.key_down()
        self.assertEqual(list(view.screen_items()), ["1", "10", "11"])
        self.assertEqual(view.selected_idx, 1)
        self.assertEqual(view.selected_item(), "10")
        self.assertEqual(view.screen_selected_line(), 1)
        view.typed("9")
        self.assertEqual(list(view.screen_items()), ["19"])
        self.assertEqual(view.selected_item(), "19")
        self.assertEqual(view.screen_selected_line(), 0)
        view.key_backspace()
        self.assertEqual(list(view.screen_items()), ["17", "18", "19"])
        self.assertEqual(view.selected_item(), "19")
        self.assertEqual(view.screen_selected_line(), 2)

    def test_screen_pg(self):
        itemlist = [str(i) for i in range(0, 6)]
        view = tuzue.view.View(items=itemlist)
        view.screen_height_set(3)
        view.key_pgdown()
        self.assertEqual(list(view.screen_items()), ["2", "3", "4"])
        self.assertEqual(view.selected_item(), "2")
        view.key_pgup()
        self.assertEqual(list(view.screen_items()), ["0", "1", "2"])
        self.assertEqual(view.selected_item(), "2")
        view.key_pgdown()
        view.key_pgdown()
        self.assertEqual(list(view.screen_items()), ["3", "4", "5"])
        self.assertEqual(view.selected_item(), "5")
        view.key_pgup()
        view.key_pgup()
        view.key_pgup()
        self.assertEqual(list(view.screen_items()), ["0", "1", "2"])
        self.assertEqual(view.selected_item(), "0")

    def test_screen_homeend(self):
        itemlist = [str(i) for i in range(0, 6)]
        view = tuzue.view.View(items=itemlist)
        view.screen_height_set(3)
        view.key_end()
        self.assertEqual(list(view.screen_items()), ["3", "4", "5"])
        self.assertEqual(view.selected_item(), "5")
        view.key_home()
        self.assertEqual(list(view.screen_items()), ["0", "1", "2"])
        self.assertEqual(view.selected_item(), "0")
