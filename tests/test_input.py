# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import tuzue.input

import unittest


class TestInput(unittest.TestCase):
    def test_backspace(self):
        input = tuzue.input.Input()
        for c in "test":
            input.typed(c)
        self.assertEqual(input.string, "test")
        input.key_backspace()
        self.assertEqual(input.string, "tes")

    def test_arrows_backspace(self):
        input = tuzue.input.Input("test")
        self.assertEqual(input.string, "test")
        input.key_left()
        input.key_backspace()
        self.assertEqual(input.string, "tet")
        input.key_left()
        input.key_left()
        input.key_backspace()
        self.assertEqual(input.string, "tet")
        input.key_right()
        input.key_backspace()
        self.assertEqual(input.string, "et")

    def test_arrows_delete(self):
        input = tuzue.input.Input("tst")
        self.assertEqual(input.string, "tst")
        input.key_delete()
        self.assertEqual(input.string, "tst")
        input.key_left()
        input.key_delete()
        self.assertEqual(input.string, "ts")
        input.key_delete()
        self.assertEqual(input.string, "ts")
        input.key_left()
        input.key_left()
        input.key_delete()
        self.assertEqual(input.string, "s")
        input.key_delete()
        input.key_delete()
