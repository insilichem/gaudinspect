#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import


from PyQt4 import QtGui
from PyQt4.QtCore import Qt


def get():
    return GAUDInspectViewResults()


class GAUDInspectViewResults(QtGui.QWidget):

    def __init__(self):
        super(GAUDInspectViewResults, self).__init__()
        # self.parent = parent
        self.title = "Results"
        self.initUI()

    def initUI(self):
        ###
        # Tab 4 - View results
        ###
        self.grid = QtGui.QGridLayout(self)

        self.infotip = QtGui.QLabel(
            "<center>Drag your file here to load results</center>")
        self.grid.addWidget(self.infotip, 0, 0)

        self.table = QtGui.QTableView()
        self.grid.addWidget(self.table, 1, 0)
        # Configure table
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        # Add filter widget
        self.filter_group = GAUDInspectViewResultsFilter('Filter results')
        self.grid.addWidget(self.filter_group, 2, 0)


class GAUDInspectViewResultsFilter(QtGui.QGroupBox):

    def __init__(self, title=None):
        super(GAUDInspectViewResultsFilter, self).__init__(title)
        self.filters = []
        self.hide()
        self.initUI()

    def initUI(self):
        self.layout = QtGui.QVBoxLayout(self)
        self.topbuttons = QtGui.QHBoxLayout()
        self.layout.addLayout(self.topbuttons)

        self.filter_btn = QtGui.QPushButton('Filter')
        self.filter_add = QtGui.QPushButton('Add')
        self.filter_clear = QtGui.QPushButton('Clear')
        self.topbuttons.addWidget(self.filter_btn)
        self.topbuttons.addWidget(self.filter_add)
        self.topbuttons.addWidget(self.filter_clear)
        self.topbuttons.addStretch(1)
        self.filter_add.clicked.connect(self.add_filter_bar)
        self.filter_clear.clicked.connect(self.clear_all)

    def filter_bar(self):
        w = QtGui.QWidget()
        w.setContentsMargins(0, 0, 0, 0)
        bar = QtGui.QHBoxLayout(w)
        bar.setContentsMargins(0, 0, 0, 0)
        w.type = QtGui.QComboBox()
        w.type.addItems(['Genes', 'Objectives'])
        w.key = QtGui.QComboBox()
        w.key.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        w.operator = QtGui.QComboBox()
        w.operator.addItems(['>', '>=', '<', '<=', '==', '!=', 'contains'])
        w.value = bar.value = QtGui.QLineEdit()
        w.btn = QtGui.QPushButton('-')
        w.btn.setFixedWidth(20)
        w.btn.clicked.connect(lambda: self.del_filter_bar(w))
        [bar.addWidget(x) for x in (w.type, w.key,
                                    w.operator, w.value, w.btn)]
        return w

    def add_filter_bar(self):
        f = self.filter_bar()
        self.filters.append(f)
        self.layout.addWidget(f)

    def del_filter_bar(self, f):
        self.layout.removeWidget(f)
        self.filters.remove(f)
        f.close()

    def clear_all(self):
        for f in self.filters:
            self.layout.removeWidget(f)
            f.close()
        del self.filters[:]
