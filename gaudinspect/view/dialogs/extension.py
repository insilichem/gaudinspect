#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import


from PyQt4 import QtGui, QtCore
import yaml


class GAUDInspectConfigureExtension(QtGui.QDialog):

    def __init__(self, parent=None):
        super(GAUDInspectConfigureExtension, self).__init__(parent=parent)
        self.setWindowTitle("Configure extension - GAUDInspect")
        self.setModal(True)
        self.initUI()

    def initUI(self):
        self.layout = QtGui.QVBoxLayout(self)

        self.general_group = QtGui.QGroupBox('General')
        self.general_layout = QtGui.QGridLayout(self.general_group)
        self.layout.addWidget(self.general_group)
        self.name_lbl = QtGui.QLabel('Name')
        self.name_fld = QtGui.QLineEdit()
        self.name_fld.setPlaceholderText("Required")
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
        self.table = QtGui.QTableWidget(0, 2)
        self.params_layout.addWidget(self.table)
        self.table.setHorizontalHeaderLabels(['Parameter', 'Value'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("QToolTip { width: 150px}")
        self.table.setSelectionMode(self.table.NoSelection)
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.RestoreDefaults | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        # Validators
        not_empty_rx = QtCore.QRegExp("\\S+")
        not_empty_validator = QtGui.QRegExpValidator(not_empty_rx, self)
        self.name_fld.setValidator(not_empty_validator)
        self.fields_to_validate = [self.name_fld]

    def showEvent(self, event):
        super(GAUDInspectConfigureExtension, self).showEvent(event)
        w, h = self.table.size().toTuple()
        w2, h2 = self.general_group.size().toTuple()
        w3, h3 = self.buttons.size().toTuple()
        self.resize(w2 + 20, h + h2 + 100)

    def done(self, r):
        if r == self.Accepted and not self.validate():
            return
        super(GAUDInspectConfigureExtension, self).done(r)
        return

    # Controller
    def validate(self):
        for field in self.fields_to_validate:
            result, text, position = field.validator().validate(field.text(), 0)
            if result != QtGui.QValidator.Acceptable:
                return False
        return True

    def load_data(self, name=None, module=None, params=None):
        if not name:
            name = ''
        if not module:
            module = ''
        if not params:
            params = {}

        self.name_fld.setText(name)
        self.module_fld.setText(module)
        params.pop('file', None)
        params.pop('module', None)
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
            params[k.text()] = yaml.load(self.table.item(i, 1).text())
        params['name'] = self.name_fld.text()
        params['module'] = self.module_fld.text()
        return params

    @staticmethod
    def process(parent, definitions, values=None):
        if values:
            name = values.pop('name', '')
            module = values.pop('module', '')
            for k in values:
                if k in definitions:
                    definitions[k][2] = values[k]
        else:
            name = ''
            module = definitions.get('module', '')
        dialog = GAUDInspectConfigureExtension(parent=parent)
        dialog.load_data(name=name, module=module, params=definitions)
        accepted = dialog.Accepted
        result = dialog.exec_()
        params = dialog.dump()
        dialog.deleteLater()
        return params, result == accepted
