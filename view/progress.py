#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui


def get(parent=None):
    return GAUDInspectViewProgress(parent=parent)


class GAUDInspectViewProgress(QtGui.QWidget):

    def __init__(self, parent=None):
        super(GAUDInspectViewProgress, self).__init__()
        self.parent = parent
        self.title = "Progress"
        self.initUI()

    def initUI(self):
        ###
        # Tab 2 - Progress of the essay
        ###
        self.grid = QtGui.QGridLayout(self)

        self.table = QtGui.QTableWidget(10, 8)
        self.grid.addWidget(self.table, 0, 0, 1, 2)
        table_headers = ['Generation', 'Evaluations',
                         'Objective 1', 'Objective 2', 'Objective 3',
                         'Objective 4', 'Objective 5', 'Objective 6', ]
        self.table.setHorizontalHeaderLabels(table_headers)

        self.chart_group = QtGui.QGroupBox('Charts')
        self.chart_layout = QtGui.QHBoxLayout(self.chart_group)
        self.grid.addWidget(self.chart_group, 1, 0)
        self.pixmap = QtGui.QPixmap('chart.png')
        self.image = QtGui.QLabel()
        self.image.setPixmap(self.pixmap)
        self.chart_layout.addWidget(self.image)

        self.btn_layout = QtGui.QVBoxLayout()
        self.grid.addLayout(self.btn_layout, 1, 1)
        self.btn_layout.addStretch(1)
        [self.btn_layout.addWidget(QtGui.QPushButton(txt)) for txt in
         ('Pause', 'Resume', 'Stop', 'Save state', 'More details')]

        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setValue(40)
        self.grid.addWidget(self.progressbar, 2, 0, 1, 2)
