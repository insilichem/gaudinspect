#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui


def get(parent=None):
    return GAUDInspectViewViewer(parent=parent)


class GAUDInspectViewViewer(QtGui.QLabel):

    def __init__(self, parent=None):
        super(GAUDInspectViewViewer, self).__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Main widget - the viewer
        self.setStyleSheet("background-color: black")
        self.setMinimumWidth(400)
        self.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.setGeometry(0, 0, 400, 400)
