#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PySide import QtGui, QtCore


class GAUDInspectConfiguration(QtGui.QDialog):

    def __init__(self, parent=None):
        super(GAUDInspectConfiguration, self).__init__(parent=parent)
        self.setWindowTitle("Edit configuration - GAUDInspect")
        self.setModal(True)
        self.initUI()

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
        self.general_gaudipath = self.browse_field(
            'GAUDI', self.tab_general_group_layout)

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
            'Background color', self.tab_viewer_group_layout)
        # BOTTOM BUTTONS
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def text_field(self, label, layout):
        w = QtGui.QWidget(self)
        wlayout = QtGui.QHBoxLayout(w)
        w.lbl = QtGui.QLabel(label)
        w.fld = QtGui.QLineEdit()
        w.fld.setMinimumWidth(300)
        for x in (w.lbl, w.fld):
            wlayout.addWidget(x)
        layout.addWidget(w)
        return w

    def browse_field(self, label, layout):
        w = QtGui.QWidget(self)
        wlayout = QtGui.QHBoxLayout(w)
        w.lbl = QtGui.QLabel(label)
        w.fld = QtGui.QLineEdit()
        w.fld.setMinimumWidth(300)
        w.btn = QtGui.QPushButton('...')
        w.btn.clicked.connect(lambda: self.get_path(w))
        for x in (w.lbl, w.fld, w.btn):
            wlayout.addWidget(x)
        layout.addWidget(w)
        return w

    def get_path(self, w):
        title = w.lbl.text()
        path, f = QtGui.QFileDialog.getOpenFileName(self, 'Locate the path to {}'.format(title),
                                                    os.getcwd(), "All files (*)")
        w.fld.setText(path)

    def load_settings(self):
        # PSEUDOCODE!!
        settings = self.parent.app.settings
        for setting in settings:
            key, val = setting.label.split("/")
            try:
                w = getattr(self, "{}_{}".format(key, val))
            except AttributeError:
                pass
            else:
                w.fld.setText(setting.value)

    def save_settings(self):
        settings = self.parent.app.settings
        for setting in settings:
            key, val = setting.label.split("/")
            try:
                w = getattr(self, "{}_{}".format(key, val))
            except AttributeError:
                pass
            else:
                setting.setValue(setting.label, w.fld.text())
