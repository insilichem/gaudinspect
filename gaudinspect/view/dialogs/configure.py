#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml

from PySide import QtGui, QtCore
from ... import configuration


class GAUDInspectConfiguration(QtGui.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Edit configuration - GAUDInspect")
        self.setModal(True)
        self.settings = QtCore.QSettings()
        self.initUI()
        self.load_settings()

    def showEvent(self, event):
        super().showEvent(event)
        self.adjustSize()

    def initUI(self):
        self.layout = QtGui.QVBoxLayout(self)

        self.tabber = QtGui.QTabWidget(self)
        self.layout.addWidget(self.tabber)

        # TAB 1 - General Settings
        self.tab_general = QtGui.QWidget(self)
        self.tabber.addTab(self.tab_general, 'General')
        self.tab_general_layout = QtGui.QVBoxLayout(self.tab_general)
        # TAB 1 - Box 1: Paths
        self.tab_general_group = QtGui.QGroupBox('Paths')
        self.tab_general_layout.addWidget(self.tab_general_group)
        self.tab_general_group_layout = QtGui.QVBoxLayout(
            self.tab_general_group)
        # Fields
        self.paths_gaudi = self.browse_field(
            self, 'GAUDI', self.tab_general_group_layout)
        self.paths_chimera = self.browse_field(
            self, 'Chimera', self.tab_general_group_layout)

        # TAB 2 - Viewer Settings
        self.tab_viewer = QtGui.QWidget(self)
        self.tabber.addTab(self.tab_viewer, 'Viewer')
        self.tab_viewer_layout = QtGui.QVBoxLayout(self.tab_viewer)
        # TAB 2 - Box 1: Paths
        self.tab_viewer_group = QtGui.QGroupBox('Viewer options')
        self.tab_viewer_layout.addWidget(self.tab_viewer_group)
        self.tab_viewer_group_layout = QtGui.QVBoxLayout(
            self.tab_viewer_group)
        self.viewer_backgroundcolor = self.text_field(
            'Background', self.tab_viewer_group_layout)

        # BOTTOM BUTTONS
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.RestoreDefaults,
            QtCore.Qt.Horizontal, self)
        self.layout.addWidget(self.buttons)
        # Button signals
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.button(QtGui.QDialogButtonBox.RestoreDefaults).clicked.connect(
            self.restore_settings)

    def text_field(self, label, layout):
        w = QtGui.QWidget(self)
        wlayout = QtGui.QHBoxLayout(w)
        wlayout.setContentsMargins(0, 0, 0, 0)

        w.lbl = QtGui.QLabel(label)
        w.lbl.setFixedWidth(100)
        w.fld = QtGui.QLineEdit()
        w.fld.setMinimumWidth(300)

        for x in (w.lbl, w.fld):
            wlayout.addWidget(x)
        layout.addWidget(w)

        return w

    @staticmethod
    def browse_field(parent, label, layout):
        """
        A helper method to create browse fields
        """
        def get_path(w):
            title = w.lbl.text()
            path, f = QtGui.QFileDialog.getOpenFileName(
                parent, 'Locate the path to {}'.format(title),
                os.getcwd(), "All files (*)")
            if path:
                w.fld.setText(path)

        w = QtGui.QWidget(parent)
        wlayout = QtGui.QHBoxLayout(w)
        wlayout.setContentsMargins(0, 0, 0, 0)

        w.lbl = QtGui.QLabel(label)
        w.lbl.setFixedWidth(100)
        w.fld = QtGui.QLineEdit()
        w.fld.setMinimumWidth(300)
        w.btn = QtGui.QPushButton('...')
        w.btn.setFixedWidth(25)
        w.btn.clicked.connect(lambda: get_path(w))

        for x in (w.lbl, w.fld, w.btn):
            wlayout.addWidget(x)
        layout.addWidget(w)

        return w

    def load_settings(self):

        for key in self.settings.allKeys():
            if not key.startswith("_"):
                k1, k2 = [s.lower() for s in key.split("/")]
                try:
                    val = getattr(self, "{}_{}".format(k1, k2))
                except AttributeError:
                    pass
                else:
                    val.fld.setText(str(self.settings.value(key)))

    def save_settings(self):
        self.settings.setValue("flags/configured", True)
        for key in self.settings.allKeys():
            if not key.startswith("_"):
                k1, k2 = [s.lower() for s in key.split("/")]
                try:
                    val = getattr(self, "{}_{}".format(k1, k2))
                except AttributeError:
                    pass
                else:
                    self.settings.setValue(key, yaml.load(val.fld.text()))
        self.settings.sync()

    def restore_settings(self):
        returned = QtGui.QMessageBox.question(
            self, "Are your sure?",
            "All parameters will be overriden with default values. "
            "This action cannot be undone. Are you sure?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if returned == QtGui.QMessageBox.Yes:
            for k, v in configuration.default.items():
                self.settings.setValue(k, v)
            self.settings.sync()
            self.load_settings()

    @staticmethod
    def process(parent=None):
        dialog = GAUDInspectConfiguration(parent)
        returned = dialog.exec_()
        if returned == dialog.Accepted:
            dialog.save_settings()
        dialog.deleteLater()
