#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import


from PyQt4 import QtGui


def get():
    return GAUDInspectViewProgress()


class GAUDInspectViewProgress(QtGui.QWidget):

    def __init__(self):
        super(GAUDInspectViewProgress, self).__init__()
        # self.parent = parent
        self.title = "Progress"
        self.initUI()

    def initUI(self):
        ###
        # Tab 2 - Progress of the essay
        ###
        self.grid = QtGui.QGridLayout(self)
        self.input_box = QtGui.QGroupBox('Input file')
        self.grid.addWidget(self.input_box, 0, 0)
        self.input_lay = QtGui.QHBoxLayout(self.input_box)
        self.input_fld = QtGui.QComboBox()
        self.input_fld.setMaxCount(10)
        self.input_fld.setEditable(True)
        self.input_fld.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.input_fld.setDuplicatesEnabled
        self.input_btn = QtGui.QPushButton('...')
        self.input_btn.setFixedWidth(40)
        self.input_run = QtGui.QPushButton('Run')
        self.input_run.setFixedWidth(40)
        self.input_lay.addWidget(self.input_fld)
        self.input_lay.addWidget(self.input_btn)
        self.input_lay.addWidget(self.input_run)

        self.tabber = QtGui.QTabWidget()
        self.table = QtGui.QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.grid.addWidget(self.table, 1, 0)

        self.textbox = QtGui.QTextEdit(self)
        self.textbox.setFontFamily('Monospace')
        self.textbox.setReadOnly(True)
        self.textbox.setWordWrapMode(QtGui.QTextOption.NoWrap)

        self.grid.addWidget(self.tabber, 1, 0)
        self.tabber.addTab(self.table, 'Tabulated data')
        self.tabber.addTab(self.textbox, 'Raw output')

        self.btn_layout = QtGui.QHBoxLayout()
        self.grid.addLayout(self.btn_layout, 2, 0)
        self.btn_layout.addStretch(1)
        [self.btn_layout.addWidget(QtGui.QPushButton(txt)) for txt in
         ('Pause', 'Resume', 'Stop', 'Save state', 'More details')]
        self.btn_layout.addStretch(1)

        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setMinimum(0)
        self.progressbar.setValue(0)
        self.progressbar.hide()
        self.grid.addWidget(self.progressbar, 3, 0)
