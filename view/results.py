#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui


def get(parent=None):
    return GAUDInspectViewResults(parent=parent)


class GAUDInspectViewResults(QtGui.QWidget):

    def __init__(self, parent=None):
        super(GAUDInspectViewResults, self).__init__()
        self.parent = parent
        self.title = "Results"
        self.initUI()

    def initUI(self):
        ###
        # Tab 4 - View results
        ###
        self.grid = QtGui.QGridLayout(self)

        self.table = QtGui.QTableWidget(30, 7)
        self.grid.addWidget(self.table, 0, 0)
        table_headers = ['Individual',
                         'Objective 1', 'Objective 2', 'Objective 3',
                         'Objective 4', 'Objective 5', 'Objective 6', ]
        self.table.setHorizontalHeaderLabels(table_headers)
        self.table.verticalHeader().setVisible(False)

        self.filter_group = GAUDInspectViewResultsFilter('Filter results')
        self.grid.addWidget(self.filter_group, 1, 0)


class GAUDInspectViewResultsFilter(QtGui.QGroupBox):

    def __init__(self, title=None):
        super(GAUDInspectViewResultsFilter, self).__init__(title)
        self.filters = set()
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
        bar.type = QtGui.QComboBox()
        bar.type.addItems(['--Choose--', 'Gene', 'Objective'])
        bar.key = QtGui.QComboBox()
        bar.key.addItems(['--Select--', 'A', 'B', 'C'])
        bar.operator = QtGui.QComboBox()
        bar.operator.addItems(['>', '<', '>=', '<=', '='])
        bar.value = QtGui.QLineEdit()
        bar.btn = QtGui.QPushButton('-')
        bar.btn.setFixedWidth(20)
        bar.btn.clicked.connect(lambda: self.del_filter_bar(w))
        [bar.addWidget(x) for x in (bar.type, bar.key,
                                    bar.operator, bar.value, bar.btn)]
        return w

    def add_filter_bar(self):
        f = self.filter_bar()
        self.filters.add(f)
        self.layout.addWidget(f)

    def del_filter_bar(self, f):
        self.layout.removeWidget(f)
        self.filters.remove(f)
        f.close()

    def clear_all(self):
        for f in self.filters:
            self.layout.removeWidget(f)
            f.close()
        self.filters.clear()
