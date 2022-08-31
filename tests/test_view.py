# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import tuzue.view

import unittest


class TestView(unittest.TestCase):
    def setUp(self):
        self.view = tuzue.view.View()

    def test_input(self):
        for c in "test":
            self.view.typed(c)
        self.assertEqual(self.view.input_string, "test")
        self.view.key_backspace()
        self.assertEqual(self.view.input_string, "tes")
