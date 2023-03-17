# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import tuzue.binput

import unittest


class TestInput(unittest.TestCase):
    def test_backspace(self):
        binput = tuzue.binput.Binput()
        for c in "test":
            binput.typed(c)
        self.assertEqual(binput.string, "test")
        binput.key_backspace()
        self.assertEqual(binput.string, "tes")

    def test_arrows_backspace(self):
        binput = tuzue.binput.Binput("test")
        self.assertEqual(binput.string, "test")
        binput.key_left()
        binput.key_backspace()
        self.assertEqual(binput.string, "tet")
        binput.key_left()
        binput.key_left()
        binput.key_backspace()
        self.assertEqual(binput.string, "tet")
        binput.key_right()
        binput.key_backspace()
        self.assertEqual(binput.string, "et")

    def test_arrows_delete(self):
        binput = tuzue.binput.Binput("tst")
        self.assertEqual(binput.string, "tst")
        binput.key_delete()
        self.assertEqual(binput.string, "tst")
        binput.key_left()
        binput.key_delete()
        self.assertEqual(binput.string, "ts")
        binput.key_delete()
        self.assertEqual(binput.string, "ts")
        binput.key_left()
        binput.key_left()
        binput.key_delete()
        self.assertEqual(binput.string, "s")
        binput.key_delete()
        binput.key_delete()

    def test_boleol_delete(self):
        binput = tuzue.binput.Binput("tst")
        self.assertEqual(binput.string, "tst")
        binput.key_bol()
        self.assertEqual(binput.string, "tst")
        binput.key_delete()
        self.assertEqual(binput.string, "st")
        binput.key_eol()
        binput.key_backspace()
        self.assertEqual(binput.string, "s")

    def test_killbol(self):
        binput = tuzue.binput.Binput("asdf zxcv")
        for i in range(5):
            binput.key_left()
        binput.key_killbol()
        self.assertEqual(binput.string, " zxcv")

    def test_killeol(self):
        binput = tuzue.binput.Binput("asdf zxcv")
        for i in range(4):
            binput.key_left()
        binput.key_killeol()
        self.assertEqual(binput.string, "asdf ")
