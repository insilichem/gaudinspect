#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PySide import QtGui, QtCore
from ... import configuration


class GAUDInspectConfiguration(QtGui.QDialog):

    def __init__(self, parent=None):
        super(GAUDInspectConfiguration, self).__init__(parent=parent)
        self.setWindowTitle("Edit configuration - GAUDInspect")
        self.setModal(True)
        self.initUI()
        self.load_settings()

    def showEvent(self, event):
        super(GAUDInspectConfiguration, self).showEvent(event)
        self.adjustSize()

    def initUI(self):
        self.canvas = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self.canvas)

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
        self.general_gaudipath = self.browse_field(
            'GAUDI', self.tab_general_group_layout)
        self.general_chimerapath = self.browse_field(
            'Chimera', self.tab_general_group_layout)

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

    def browse_field(self, label, layout):
        w = QtGui.QWidget(self)
        wlayout = QtGui.QHBoxLayout(w)
        wlayout.setContentsMargins(0, 0, 0, 0)

        w.lbl = QtGui.QLabel(label)
        w.lbl.setFixedWidth(100)
        w.fld = QtGui.QLineEdit()
        w.fld.setMinimumWidth(300)
        w.btn = QtGui.QPushButton('...')
        w.btn.setFixedWidth(25)
        w.btn.clicked.connect(lambda: self.get_path(w))

        for x in (w.lbl, w.fld, w.btn):
            wlayout.addWidget(x)
        layout.addWidget(w)

        return w

    def get_path(self, w):
        title = w.lbl.text()
        path, f = QtGui.QFileDialog.getOpenFileName(
            self, 'Locate the path to {}'.format(title),
            os.getcwd(), "All files (*)")
        if path:
            w.fld.setText(path)

    def load_settings(self):
        settings = self.parent().app.settings
        for key in settings.allKeys():
            k1, k2 = [s.lower() for s in key.split("/")]
            try:
                val = getattr(self, "{}_{}".format(k1, k2))
            except AttributeError:
                pass
            else:
                val.fld.setText(str(settings.value(key)))

    def save_settings(self):
        settings = self.parent().app.settings
        settings.setValue("general/configured", True)
        for key in settings.allKeys():
            k1, k2 = [s.lower() for s in key.split("/")]
            try:
                val = getattr(self, "{}_{}".format(k1, k2))
            except AttributeError:
                pass
            else:
                settings.setValue(key, val.fld.text())

    def restore_settings(self):
        returned = QtGui.QMessageBox.question(
            self, "Are your sure?",
            "All parameters will be overriden with default values. Are you sure?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if returned == QtGui.QMessageBox.Yes:
            settings = self.parent().app.settings
            for k, v in configuration.default.items():
                settings.setValue(k, v)
            self.load_settings()
