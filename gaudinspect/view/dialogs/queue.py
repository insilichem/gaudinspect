#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import


from PyQt4 import QtGui


class GAUDInspectQueueDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(GAUDInspectQueueDialog, self).__init__(parent=parent)

        self.setWindowTitle("Job Queue - GAUDInspect")
        self.setModal(False)
        self.initUI()
        self.signals()

    def show(self):
        super(GAUDInspectQueueDialog, self).show()
        self.activateWindow()
        self.raise_()
        self.setFocus()

    def showEvent(self, event):
        super(GAUDInspectQueueDialog, self).showEvent(event)
        self.adjustSize()

    def initUI(self):
        self.setMinimumWidth(600)
        self.layout = QtGui.QVBoxLayout(self)

        self.box = QtGui.QGroupBox("Job Queue")
        self.box_lay = QtGui.QHBoxLayout(self.box)
        self.layout.addWidget(self.box)

        self.table = QtGui.QTableWidget(0, 2)
        self.table.setSortingEnabled(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setHorizontalHeaderLabels(["Path", "Status"])
        self.table.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.table.resizeColumnsToContents()
        self.box_lay.addWidget(self.table)

        self.tools_lay = QtGui.QVBoxLayout()
        self.box_lay.addLayout(self.tools_lay)
        self.add_job = QtGui.QPushButton("Load job")
        self.del_job = QtGui.QPushButton("Remove")
        self.del_all = QtGui.QPushButton("Remove all")
        self.start_queue = QtGui.QPushButton("Start")
        self.stop_queue = QtGui.QPushButton("Stop")

        self.tools_lay.addWidget(self.add_job)
        self.tools_lay.addWidget(self.del_job)
        self.tools_lay.addWidget(self.del_all)
        self.tools_lay.addStretch(1)
        self.tools_lay.addWidget(self.start_queue)
        self.tools_lay.addWidget(self.stop_queue)

    def signals(self):
        pass
