#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui


def get(parent=None):
    return GAUDInspectViewStats(parent=parent)


class GAUDInspectViewStats(QtGui.QWidget):

    def __init__(self, parent=None):
        super(GAUDInspectViewStats, self).__init__()
        self.parent = parent
        self.hide()
        self.initUI()

    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QtGui.QVBoxLayout(self)
        self.chart_group = QtGui.QGroupBox('Charts')
        self.chart_layout = QtGui.QVBoxLayout(self.chart_group)
        self.layout.addWidget(self.chart_group, 1, 0)

        self.pixmap = QtGui.QPixmap('chart.png')
        self.image = QtGui.QLabel()
        self.image.setPixmap(self.pixmap)
        self.chart_layout.addWidget(self.image)

        # Disable margins
        for obj in (self, self.chart_group, self.layout):
            try:
                obj.setContentsMargins(0, 0, 0, 0)
                obj.setSpacing(0)
            except AttributeError:
                pass
