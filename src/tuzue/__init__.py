# Copyright (C) 2022 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.

import importlib.metadata

import tuzue.inspector
import tuzue.ui.tcurses
import tuzue.view


def version():
    return importlib.metadata.version("tuzue")


def navigate(struct, title=""):
    view = tuzue.view.View(items=struct, title=title)
    done = None
    with tuzue.ui.tcurses.context() as ui:
        while not done:
            ui.show(view)
            done = ui.interact(view)
    return view.selected_item()


def inspect(*args, **kwargs):
    return tuzue.inspector.inspect(*args, **kwargs)
