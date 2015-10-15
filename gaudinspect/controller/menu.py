#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from functools import partial

from PySide.QtGui import QFileDialog, QAction
from .base import GAUDInspectBaseChildController
from ..view.dialogs.configure import GAUDInspectConfiguration
from ..view.dialogs.about import GAUDInspectAboutDialog


class GAUDInspectMenuController(GAUDInspectBaseChildController):

    def __init__(self, recent_model=None, **kwargs):
        super().__init__(**kwargs)
        self.recent = recent_model

        self.menu = self.view.menu
        self.actions()
        self.slots()
        self.signals()

    def actions(self):
        self.populate_open_recent()

    def signals(self):
        # Menu item triggers
        self.menu.file.open.triggered.connect(self.open_file_dialog.exec_)
        self.menu.file.exit.triggered.connect(self.parent().app.exit)

        self.menu.edit.configuration.triggered.connect(
            self.configure_dialog)

        self.menu.viewer.enable_fx.triggered.connect(
            self.parent().view.viewer.enable_effects)
        self.menu.viewer.disable_fx.triggered.connect(
            self.parent().view.viewer.disable_effects)

        self.menu.help.about.triggered.connect(self.about_dialog.exec_)

        # Open recent behaviour
        self.recent.myDataChanged.connect(self.populate_open_recent)

    def slots(self):
        self.open_file_dialog = self._open_file_dialog()
        self.configure_dialog = self._configure
        self.about_dialog = GAUDInspectAboutDialog(self.view)

    # Private methods
    def _open_file_dialog(self):
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

    def populate_open_recent(self, *args):
        self.menu.file.open_recent.clear()
        items = self.recent.all_items()
        if items:
            for path, timestamp in items[:15]:
                action = QAction(self._trim(path), self.menu.file.open_recent)
                self.menu.file.open_recent.addAction(action)
                action.triggered.connect(partial(self.parent().open_file, path))

            self.menu.file.open_recent.addSeparator()
            # Clear All action
            self.menu.file.open_recent.clear_all = QAction(
                'Clear all', self.menu.file.open_recent)
            self.menu.file.open_recent.clear_all.triggered.connect(self.recent.clear_all)
            self.menu.file.open_recent.addAction(self.menu.file.open_recent.clear_all)
            # Clear Deleted action
            self.menu.file.open_recent.clear_deleted = QAction(
                'Clear deleted', self.menu.file.open_recent)
            self.menu.file.open_recent.clear_deleted.triggered.connect(self.recent.clear_deleted)
            self.menu.file.open_recent.addAction(self.menu.file.open_recent.clear_deleted)

    @staticmethod
    def _trim(s, maxlength=50, start=10):
        """
        Trims a string to desired `length`, inserting ... after `start` chars
        """
        if s and len(s) > maxlength:
            return s[:start] + '...' + s[-(maxlength - start - 3):]
        return s
