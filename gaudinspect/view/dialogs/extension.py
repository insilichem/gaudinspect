#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore


class GAUDInspectConfigureExtension(QtGui.QDialog):

    def __init__(self, parent=None):
        super(GAUDInspectConfigureExtension, self).__init__(parent=parent)
        self.setWindowTitle("Configure extension - GAUDInspect")
        self.setModal(True)
        self.initUI()

    def initUI(self):
        self.canvas = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self.canvas)

        self.general_group = QtGui.QGroupBox('General')
        self.general_layout = QtGui.QGridLayout(self.general_group)
        self.layout.addWidget(self.general_group)
        self.name_lbl = QtGui.QLabel('Name')
        self.name_fld = QtGui.QLineEdit()
        self.name_fld.setPlaceholderText("Name it, please")
        self.module_lbl = QtGui.QLabel('Module')
        self.module_fld = QtGui.QLineEdit()
        self.module_fld.setEnabled(False)
        self.general_layout.addWidget(self.name_lbl, 0, 0)
        self.general_layout.addWidget(self.name_fld, 0, 1)
        self.general_layout.addWidget(self.module_lbl, 1, 0)
        self.general_layout.addWidget(self.module_fld, 1, 1)

        self.params_group = QtGui.QGroupBox('Parameters')
        self.params_layout = QtGui.QVBoxLayout(self.params_group)
        self.layout.addWidget(self.params_group)
        self.table = QtGui.QTableWidget(self.params_group)
        self.params_layout.addWidget(self.table)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Parameter', 'Value'])
        self.table.setSizePolicy(QtGui.QSizePolicy.Preferred,
                                 QtGui.QSizePolicy.Expanding)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setFixedWidth(280)
        self.table.setStyleSheet("QToolTip { width: 150px}")
        self.table.setSelectionMode(self.table.NoSelection)

        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.RestoreDefaults | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def showEvent(self, event):
        super(GAUDInspectConfigureExtension, self).showEvent(event)
        w, h = self.table.size().toTuple()
        w2, h2 = self.general_group.size().toTuple()
        self.resize(w2 + 20, h + h2 + 85)

    # Controller
    def load_data(self, name=None, module=None, params=None):
        if not name:
            name = ''
        if not module:
            module = ''
        if not params:
            params = {}

        self.name_fld.setText(name)
        self.module_fld.setText(module)
        for i, (k, (type_, tooltip, default)) in enumerate(params.items()):
            self.table.insertRow(i)
            key = QtGui.QTableWidgetItem(str(k))
            key.type_ = type_
            key.setToolTip(tooltip)
            self.table.setItem(i, 0, key)
            val = QtGui.QTableWidgetItem(str(default))
            val.setToolTip(tooltip)
            self.table.setItem(i, 1, val)
        self.table.resizeColumnsToContents()

    def dump(self):
        params = {}
        for i in range(self.table.rowCount()):
            k = self.table.item(i, 0)
            params[k.text()] = k.type_, k.toolTip(), k.type_(
                self.table.item(i, 1).text())
        params['name'] = self.name_fld.text()
        params['module'] = self.module_fld.text()
        return params

    @staticmethod
    def process(parent, definitions, name=None, module=None, values=None):
        if values:
            for k in values:
                if k in definitions:
                    definitions[k][2] = values[k]
                    print(k, definitions[k], values[k])
        dialog = GAUDInspectConfigureExtension(parent=parent)
        dialog.load_data(name=name, module=module, params=definitions)
        result = dialog.exec_()
        params = dialog.dump()
        return params, result == dialog.Accepted