#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from PySide.QtGui import QFileDialog, QAction
from PySide import QtCore
from .base import GAUDInspectBaseChildController
from ..view.dialogs.configure import GAUDInspectConfiguration


class GAUDInspectMenuController(GAUDInspectBaseChildController):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = self.view.menu
        self.slots()
        self.signals()
        self.actions()

    def actions(self):
        self._populate_open_recent()

    def signals(self):
        self.menu.file.open.triggered.connect(self.open_file_dialog.exec_)
        self.menu.file.exit.triggered.connect(self.parent().app.exit)

        self.menu.edit.configuration.triggered.connect(
            self.configure_dialog)

        self.menu.viewer.enable_fx.triggered.connect(
            self.parent().view.viewer.enable_effects)
        self.menu.viewer.disable_fx.triggered.connect(
            self.parent().view.viewer.disable_effects)

    def slots(self):
        self.open_file_dialog = self._open_file()
        self.configure_dialog = self._configure

    # Private methods
    def _open_file(self):
        dialog = QFileDialog(self.view, "Open GAUDI file", os.getcwd(),
                             "GAUDI files (*.gaudi);; "
                             "GAUDI output (*.out.gaudi);; "
                             "GAUDI input (*.in.gaudi);; "
                             "All files (*)")
        dialog.setFileMode(QFileDialog.ExistingFile)
        return dialog

    def _configure(self):
        dialog = GAUDInspectConfiguration(self.view)
        returned = dialog.exec_()
        if returned == dialog.Accepted:
            dialog.save_settings()

    def _populate_open_recent(self):
        settings = QtCore.QSettings()
        size = settings.beginReadArray("recent_files")
        for i in range(size):
            settings.setArrayIndex(i)
            path = settings.value("input")
            action = QAction(self._trim(path), self.menu.file.open_recent)
            self.menu.file.open_recent.addAction(action)
            action.triggered.connect(lambda: self.parent()._open_file(path))
        settings.endArray()

    @staticmethod
    def _trim(s, maxlength=50, start=10):
        if len(s) > maxlength:
            return s[:start] + '...' + s[-(maxlength - start - 3):]
        return s
