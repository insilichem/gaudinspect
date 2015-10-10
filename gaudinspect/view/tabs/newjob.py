#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore
from collections import OrderedDict


def get():
    return GAUDInspectViewNewJob()


class GAUDInspectViewNewJob(QtGui.QWidget):

    def __init__(self):
        super(GAUDInspectViewNewJob, self).__init__()
        # self.parent = parent
        self.title = "New Job"
        self.dialogs()
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout(self)

        # Genes
        self.genes_label = QtGui.QLabel('Genes')
        self.grid.addWidget(self.genes_label, 0, 0)
        self.genes_list = QtGui.QListWidget()
        self.grid.addWidget(self.genes_list, 1, 0)
        # Genes buttons
        self.genes_add = QtGui.QPushButton('Add')
        self.genes_del = QtGui.QPushButton('Del')
        self.genes_cfg = QtGui.QPushButton('Config')
        self.genes_buttons = QtGui.QHBoxLayout()
        self.genes_buttons.addStretch(1)
        self.genes_buttons.addWidget(self.genes_add)
        self.genes_buttons.addWidget(self.genes_del)
        self.genes_buttons.addWidget(self.genes_cfg)
        self.genes_buttons.addStretch(1)
        self.grid.addLayout(self.genes_buttons, 2, 0)

        # Objectives
        self.objectives_label = QtGui.QLabel('Objectives')
        self.grid.addWidget(self.objectives_label, 0, 1)
        self.objectives_list = QtGui.QListWidget()
        self.grid.addWidget(self.objectives_list, 1, 1)
        # Objectives buttons
        self.objectives_add = QtGui.QPushButton('Add')
        self.objectives_del = QtGui.QPushButton('Del')
        self.objectives_cfg = QtGui.QPushButton('Config')
        self.objectives_buttons = QtGui.QHBoxLayout()
        self.objectives_buttons.addStretch(1)
        self.objectives_buttons.addWidget(self.objectives_add)
        self.objectives_buttons.addWidget(self.objectives_del)
        self.objectives_buttons.addWidget(self.objectives_cfg)
        self.objectives_buttons.addStretch(1)
        self.grid.addLayout(self.objectives_buttons, 2, 1)

        # General settings group
        self.general_group = QtGui.QGroupBox('General settings')
        self.general_grid = QtGui.QGridLayout()
        self.general_group.setLayout(self.general_grid)
        self.general_layout = QtGui.QHBoxLayout()
        self.general_layout.addWidget(self.general_group)
        self.grid.addLayout(self.general_layout, 3, 0, 1, 2)
        # Generations
        self.general_generations_label = QtGui.QLabel('Generations')
        self.general_generations_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.general_grid.addWidget(
            self.general_generations_label, 0, 0)
        self.general_generations_field = QtGui.QLineEdit(
            self.general_group)
        self.general_generations_field.setInputMask('0009')
        self.general_generations_field.setMaxLength(4)
        self.general_generations_field.setFixedWidth(50)
        self.general_grid.addWidget(
            self.general_generations_field, 0, 1)
        # Population
        self.general_population_label = QtGui.QLabel('Population')
        self.general_population_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.general_grid.addWidget(
            self.general_population_label, 1, 0)
        self.general_population_field = QtGui.QLineEdit(
            self.general_group)
        self.general_population_field.setInputMask('0009')
        self.general_population_field.setMaxLength(4)
        self.general_population_field.setFixedWidth(50)
        self.general_grid.addWidget(
            self.general_population_field, 1, 1)
        # Name of project
        self.general_project_label = QtGui.QLabel('Name')
        self.general_project_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.general_grid.addWidget(self.general_project_label, 0, 2)
        self.general_project_field = QtGui.QLineEdit(
            self.general_group)
        self.general_project_field.setMaxLength(30)
        self.general_grid.addWidget(self.general_project_field, 0, 3)
        self.general_project_btn = QtGui.QPushButton('*')
        self.general_grid.addWidget(self.general_project_btn, 0, 4)
        self.general_project_btn.setFixedWidth(30)
        # Name of output path
        self.general_outputpath_label = QtGui.QLabel('Output path')
        self.general_outputpath_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.general_grid.addWidget(
            self.general_outputpath_label, 1, 2)
        self.general_outputpath_field = QtGui.QLineEdit(
            self.general_group)
        self.general_grid.addWidget(
            self.general_outputpath_field, 1, 3)
        self.general_outputpath_browse = QtGui.QPushButton('...')
        self.general_grid.addWidget(
            self.general_outputpath_browse, 1, 4)
        self.general_outputpath_browse.setFixedWidth(30)
        # Advanced options button
        self.advanced_btn = QtGui.QPushButton('Advanced')
        self.advanced_btn.setSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        self.general_grid.addWidget(self.advanced_btn, 0, 5, 2, 1)
        self.bottom_bar = QtGui.QHBoxLayout()
        self.grid.addLayout(self.bottom_bar, 4, 0, 1, 2)
        self.bottom_save = QtGui.QPushButton('Save')
        self.bottom_bar.addWidget(self.bottom_save)
        self.bottom_bar.addStretch(1)
        self.bottom_test = QtGui.QPushButton('Test')
        self.bottom_bar.addWidget(self.bottom_test)
        self.bottom_run = QtGui.QPushButton('Run')
        self.bottom_run.setStyleSheet('font-weight: bold;')
        self.bottom_bar.addWidget(self.bottom_run)

    def dialogs(self):
        self.advanced_dialog = GAUDInspectAdvancedOptionsDialog(self)


class GAUDInspectAdvancedOptionsDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(GAUDInspectAdvancedOptionsDialog, self).__init__(parent=parent)

        self.advanced_options = {}
        self.setWindowTitle("Advanced project settings - GAUDInspect")
        self.setFixedWidth(300)
        self.setModal(True)
        self.initUI()

    def initUI(self):
        self.canvas = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self.canvas)
        self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                  QtGui.QSizePolicy.Expanding)

        # Table for parameters
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(2)
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
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(['Parameter', 'Value'])
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
        self.table.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                 QtGui.QSizePolicy.Expanding)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setFixedWidth(280)
        self.table.setStyleSheet("QToolTip { width: 150px}")
        self.table.setSelectionMode(self.table.NoSelection)

    def showEvent(self, event):
        super(GAUDInspectAdvancedOptionsDialog, self).showEvent(event)
        w, h = self.table.size().toTuple()
        self.resize(w + 20, h + 50)
