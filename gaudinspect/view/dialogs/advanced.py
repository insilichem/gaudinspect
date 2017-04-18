#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import


from copy import deepcopy
from PyQt4 import QtGui, QtCore
from ...configuration import ADVANCED_OPTIONS_DEFAULT


class GAUDInspectAdvancedOptionsDialog(QtGui.QDialog):

    def __init__(self, parent=None, data=None):
        super(GAUDInspectAdvancedOptionsDialog, self).__init__(parent=parent)

        self.advanced_options = {}
        self.setWindowTitle("Advanced project settings - GAUDInspect")
        self.setModal(True)
        self.initUI()
        self.loaded_data = data if data else deepcopy(ADVANCED_OPTIONS_DEFAULT)
        self.load_data()

    def initUI(self):
        self.layout = QtGui.QVBoxLayout(self)

        # Table for parameters
        self.table = QtGui.QTableWidget(0, 2)
        self.layout.addWidget(self.table)

        # Buttons
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok |
            QtGui.QDialogButtonBox.RestoreDefaults |
            QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.button(QtGui.QDialogButtonBox.RestoreDefaults
                            ).clicked.connect(self.restore_data)
        self.layout.addWidget(self.buttons)

    def showEvent(self, event):
        super(GAUDInspectAdvancedOptionsDialog, self).showEvent(event)
        bw, bh = self.buttons.size().toTuple()
        tw, th = self.table.size().toTuple()
        self.resize(bw + 24, bh + th + 24)

    def load_data(self, data=None):
        if data is None:
            data = self.loaded_data
        flags = QtCore.Qt.ItemFlags()
        flags != QtCore.Qt.ItemIsEditable
        black = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        for i, (k, (v, tip)) in enumerate(data.items()):
            self.table.insertRow(i)
            key = QtGui.QTableWidgetItem(str(k))
            key.setFlags(flags)
            key.setForeground(black)
            key.setToolTip(tip)
            self.table.setItem(i, 0, key)
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(v)))

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("QToolTip { width: 150px}")
        self.table.setSelectionMode(self.table.NoSelection)
        self.table.setHorizontalHeaderLabels(['Parameter', 'Value'])
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def dump_data(self):
        for i in range(self.table.rowCount()):
            key = self.table.item(i, 0).text()
            val = self.table.item(i, 1).text()
            self.loaded_data.get(key, [''])[0] = val
        return self.loaded_data

    def restore_data(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.load_data(deepcopy(ADVANCED_OPTIONS_DEFAULT))

    @staticmethod
    def process(parent, data=None):
        if data is None:
            data = deepcopy(ADVANCED_OPTIONS_DEFAULT)
        dialog = GAUDInspectAdvancedOptionsDialog(parent=parent, data=data)
        result = dialog.exec_()
        if result == dialog.Accepted:
            dialog.dump_data()
        dialog.deleteLater()
