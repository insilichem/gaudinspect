#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PySide.QtGui import QFileDialog


class GAUDInspectMenuController(object):

    def __init__(self, parent, view):
        self.parent = parent
        self.view = view
        self.menu = self.view.menu
        self.slots()
        self.signals()
        self.actions()

    def actions(self):
        pass

    def signals(self):
        self.menu.file.open.triggered.connect(self.open_file_dialog.open)
        self.menu.file.exit.triggered.connect(self.parent.app.exit)

        self.menu.viewer.enable_fx.triggered.connect(
            self.parent.view.viewer.enable_effects)
        self.menu.viewer.disable_fx.triggered.connect(
            self.parent.view.viewer.disable_effects)

    def slots(self):
        self.open_file_dialog = self._open_file()

    def _open_file(self):
        dialog = QFileDialog(self.view, "Open GAUDI file", os.getcwd(),
                             "GAUDI files (*.gaudi);; GAUDI output (*.out.gaudi);; GAUDI input (*.in.gaudi)")
        dialog.setFileMode(QFileDialog.ExistingFile)
        return dialog
