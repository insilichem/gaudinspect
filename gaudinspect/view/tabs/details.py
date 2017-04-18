#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import


from PyQt4 import QtGui


def get():
    return GAUDInspectViewDetails()


class GAUDInspectViewDetails(QtGui.QWidget):

    def __init__(self):
        super(GAUDInspectViewDetails, self).__init__()
        self.title = "Details"
        self.initUI()

    def initUI(self):
        ###
        # Tab 3 - Detailed history
        ###
        self.grid = QtGui.QGridLayout(self)

        self.warning = QtGui.QLabel(
            "<p align='center'><b>This tab in only a stub</b></p>"
            "<p align='center'><i>Deep changes need to be done in GAUDI to implement this feature.<br />"
            "Consider this a preview of future functionality.</i></p><hr />")
        self.grid.addWidget(self.warning, 0, 0, 1, 2)

        # Tab 3 - Column 1 - Select individual
        self.col1 = QtGui.QVBoxLayout()
        self.grid.addLayout(self.col1, 1, 0)
        self.col1_ind_box = QtGui.QGroupBox('Individuals')
        self.col1_ind_layout = QtGui.QVBoxLayout(self.col1_ind_box)
        self.col1.addWidget(self.col1_ind_box)
        self.col1_toolbox = QtGui.QToolBox()
        self.col1_ind_layout.addWidget(self.col1_toolbox)

        self.col1_generations = QtGui.QListWidget()
        self.col1_toolbox.addItem(self.col1_generations, 'Generations')

        self.col1_population = QtGui.QListWidget()
        self.col1_toolbox.addItem(self.col1_population, 'Individuals')

        self.col1_genes = QtGui.QWidget()
        self.col1_toolbox.addItem(self.col1_genes, 'Genes')
        self.col1_genes_layout = QtGui.QVBoxLayout(self.col1_genes)
        self.col1_genes_layout.setContentsMargins(0, 0, 0, 0)
        self.col1_genes_table = QtGui.QTableWidget(5, 3)
        self.col1_genes_layout.addWidget(self.col1_genes_table)
        self.col1_genes_table.horizontalHeader().setStretchLastSection(True)
        self.col1_genes_table.verticalHeader().setVisible(False)
        self.col1_genes_table.setColumnWidth(0, 20)
        self.col1_genes_table.setHorizontalHeaderLabels(
            ['', 'Gene', 'Allele'])
        self.col1_genes_buttons = QtGui.QHBoxLayout()
        self.col1_genes_layout.addLayout(self.col1_genes_buttons)
        self.col1_genes_express_btn = QtGui.QPushButton('(Un)express')
        self.col1_genes_buttons.addWidget(self.col1_genes_express_btn)
        self.col1_genes_express_all_btn = QtGui.QPushButton('(Un)express all')
        self.col1_genes_buttons.addWidget(self.col1_genes_express_all_btn)
        [self.col1_genes_table.setCellWidget(i, 0, QtGui.QCheckBox(''))
         for i in range(5)]

        # Tab 3 - Column 2 - the environment
        self.col2 = QtGui.QVBoxLayout()
        self.grid.addLayout(self.col2, 1, 1)
        self.col2_env_box = QtGui.QGroupBox('Environment')
        self.col2_env_layout = QtGui.QVBoxLayout(self.col2_env_box)
        self.col2.addWidget(self.col2_env_box)
        self.col2_env_table = QtGui.QTableWidget(10, 2)
        self.col2_env_table.horizontalHeader().setStretchLastSection(True)
        self.col2_env_table.setHorizontalHeaderLabels(['Objective', 'Score'])
        self.col2_env_table.verticalHeader().setVisible(False)
        self.col2_env_layout.addWidget(self.col2_env_table)
        self.col2_env_buttons = QtGui.QHBoxLayout()
        self.col2_env_layout.addLayout(self.col2_env_buttons)
        self.col2_env_evaluate = QtGui.QPushButton('Evaluate')
        self.col2_env_buttons.addWidget(self.col2_env_evaluate)
        self.col2_env_evaluate_all = QtGui.QPushButton('Evaluate all')
        self.col2_env_buttons.addWidget(self.col2_env_evaluate_all)
