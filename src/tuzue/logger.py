# Copyright (C) 2023 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
"""
Logger module for tuzue that facilitates logging configuration changes
"""

import logging

logger = logging.getLogger("tuzue")


def debug_on(filename):
    handler = logging.FileHandler(filename, mode="w")
    formatter = logging.Formatter("%(asctime)s %(message)s")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    global logger
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
