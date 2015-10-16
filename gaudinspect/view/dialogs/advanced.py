#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore


class GAUDInspectAdvancedOptionsDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.advanced_options = {}
        self.setWindowTitle("Advanced project settings - GAUDInspect")
        self.setModal(True)
        self.initUI()

    def initUI(self):
        self.layout = QtGui.QVBoxLayout(self)

        # Table for parameters
        self.table = QtGui.QTableWidget(0, 2)
        self.layout.addWidget(self.table)

        # Buttons
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.RestoreDefaults | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def fill_table(self, model):
        self.table.clear()
        flags = QtCore.Qt.ItemFlags()
        flags != QtCore.Qt.ItemIsEditable
        black = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        for i, (k, (v, tip)) in enumerate(model.items()):
            self.table.insertRow(i)
            key = QtGui.QTableWidgetItem(str(k))
            key.setFlags(flags)
            key.setForeground(black)
            key.setToolTip(tip)
            self.table.setItem(i, 0, key)
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(v)))

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("QToolTip { width: 150px}")
        self.table.setSelectionMode(self.table.NoSelection)
        self.table.setHorizontalHeaderLabels(['Parameter', 'Value'])

    def showEvent(self, event):
        super(GAUDInspectAdvancedOptionsDialog, self).showEvent(event)
        bw, bh = self.buttons.size().toTuple()
        tw, th = self.table.size().toTuple()
        self.resize(bw + 24, bh + th + 24)
