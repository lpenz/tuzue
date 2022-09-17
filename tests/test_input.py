# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import tuzue.input

import unittest


class TestInput(unittest.TestCase):
    def setUp(self):
        self.input = tuzue.input.Input()

    def test_backspace(self):
        for c in "test":
            self.input.typed(c)
        self.assertEqual(self.input.string, "test")
        self.input.key_backspace()
        self.assertEqual(self.input.string, "tes")
