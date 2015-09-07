#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore


class GAUDInspectLiveTest(QtGui.QMainWindow):

    def __init__(self):
        super(GAUDInspectLiveTest, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.initUI()
        self.show()

    def initUI(self):
        # Set up main window
        self.canvas = QtGui.QWidget(self)
        self.setCentralWidget(self.canvas)
        self.layout = QtGui.QGridLayout(self.canvas)

        self.setWindowTitle('Live Test - GAUDInspect')
        self.setGeometry(0, 0, 900, 600)
        self.center()

        # Top menu - File
        self.menu_file = self.menuBar().addMenu("&File")
        self.menu_file.addAction('New')
        self.menu_file.addAction('Open')
        self.menu_file.addAction('Save')
        self.menu_file.addSeparator()
        self.menu_file.addAction('Import state')
        self.menu_file.addAction('Export state')
        self.menu_file.addSeparator()
        self.menu_file.addAction('Exit')

        # Top menu - Edit
        self.menu_edit = self.menuBar().addMenu("&Edit")
        self.menu_edit.addAction('Project settings')
        self.menu_edit.addAction('Project file (advanced)')
        self.menu_edit.addSeparator()
        self.menu_edit.addAction('Configuration')

        # Top menu - Controls
        self.menu_controls = self.menuBar().addMenu("&Controls")
        self.menu_controls.addAction('Run')
        self.menu_controls.addAction('Finish')
        self.menu_controls.addAction('Cancel')
        self.menu_controls.addSeparator()
        self.menu_controls.addAction('Pause')
        self.menu_controls.addAction('Pause at next generation')
        self.menu_controls.addAction('Forward one generation')
        self.menu_controls.addSeparator()
        self.menu_controls.addAction('Show live stats')

        # Top menu - Help
        self.menu_help = self.menuBar().addMenu("&Help")
        self.menu_help.addAction('Help')
        self.menu_help.addAction('Website')
        self.menu_help.addSeparator()
        self.menu_help.addAction('About')

        # Main widget - the viewer
        self.viewer = QtGui.QLabel(" ")
        self.viewer.setStyleSheet("background-color: black")
        self.viewer.setMinimumWidth(400)
        self.viewer.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.viewer.setGeometry(0, 0, 400, 400)
        self.layout.addWidget(self.viewer, 0, 0)

        # Main tabber
        self.tabber = QtGui.QTabWidget()
        self.layout.addWidget(self.tabber, 0, 1)

        ###
        # Tab 1 - Prepare new job
        ###
        self.tab1 = QtGui.QWidget()
        self.tab1_grid = QtGui.QGridLayout(self.tab1)
        self.tabber.addTab(self.tab1, 'New job')

        # Genes
        self.tab1_genes_label = QtGui.QLabel('Genes')
        self.tab1_grid.addWidget(self.tab1_genes_label, 0, 0)
        self.tab1_genes_list = QtGui.QListWidget()
        self.tab1_grid.addWidget(self.tab1_genes_list, 1, 0)
        # Genes buttons
        self.tab1_genes_add = QtGui.QPushButton('Add')
        self.tab1_genes_del = QtGui.QPushButton('Del')
        self.tab1_genes_cfg = QtGui.QPushButton('Config')
        self.tab1_genes_buttons = QtGui.QHBoxLayout()
        self.tab1_genes_buttons.addStretch(1)
        self.tab1_genes_buttons.addWidget(self.tab1_genes_add)
        self.tab1_genes_buttons.addWidget(self.tab1_genes_del)
        self.tab1_genes_buttons.addWidget(self.tab1_genes_cfg)
        self.tab1_genes_buttons.addStretch(1)
        self.tab1_grid.addLayout(self.tab1_genes_buttons, 2, 0)

        # Objectives
        self.tab1_objectives_label = QtGui.QLabel('Objectives')
        self.tab1_grid.addWidget(self.tab1_objectives_label, 0, 1)
        self.tab1_objectives_list = QtGui.QListWidget(self.canvas)
        self.tab1_grid.addWidget(self.tab1_objectives_list, 1, 1)
        # Objectives buttons
        self.tab1_objectives_add = QtGui.QPushButton('Add')
        self.tab1_objectives_del = QtGui.QPushButton('Del')
        self.tab1_objectives_cfg = QtGui.QPushButton('Config')
        self.tab1_objectives_buttons = QtGui.QHBoxLayout()
        self.tab1_objectives_buttons.addStretch(1)
        self.tab1_objectives_buttons.addWidget(self.tab1_objectives_add)
        self.tab1_objectives_buttons.addWidget(self.tab1_objectives_del)
        self.tab1_objectives_buttons.addWidget(self.tab1_objectives_cfg)
        self.tab1_objectives_buttons.addStretch(1)
        self.tab1_grid.addLayout(self.tab1_objectives_buttons, 2, 1)

        # General settings group
        self.tab1_general_group = QtGui.QGroupBox('General settings')
        self.tab1_general_grid = QtGui.QGridLayout()
        self.tab1_general_group.setLayout(self.tab1_general_grid)
        self.tab1_general_layout = QtGui.QHBoxLayout()
        self.tab1_general_layout.addWidget(self.tab1_general_group)
        self.tab1_grid.addLayout(self.tab1_general_layout, 3, 0, 1, 2)
        # Generations
        self.tab1_general_generations_label = QtGui.QLabel('Generations')
        self.tab1_general_generations_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tab1_general_grid.addWidget(
            self.tab1_general_generations_label, 0, 0)
        self.tab1_general_generations_field = QtGui.QLineEdit(
            self.tab1_general_group)
        self.tab1_general_generations_field.setInputMask('0009')
        self.tab1_general_generations_field.setMaxLength(4)
        self.tab1_general_generations_field.setFixedWidth(50)
        self.tab1_general_grid.addWidget(
            self.tab1_general_generations_field, 0, 1)
        # Population
        self.tab1_general_population_label = QtGui.QLabel('Population')
        self.tab1_general_population_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tab1_general_grid.addWidget(
            self.tab1_general_population_label, 1, 0)
        self.tab1_general_population_field = QtGui.QLineEdit(
            self.tab1_general_group)
        self.tab1_general_population_field.setInputMask('0009')
        self.tab1_general_population_field.setMaxLength(4)
        self.tab1_general_population_field.setFixedWidth(50)
        self.tab1_general_grid.addWidget(
            self.tab1_general_population_field, 1, 1)
        # Name of project
        self.tab1_general_project_label = QtGui.QLabel('Name')
        self.tab1_general_project_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tab1_general_grid.addWidget(self.tab1_general_project_label, 0, 2)
        self.tab1_general_project_field = QtGui.QLineEdit(
            self.tab1_general_group)
        self.tab1_general_project_field.setMaxLength(15)
        self.tab1_general_grid.addWidget(self.tab1_general_project_field, 0, 3)
        self.tab1_general_project_btn = QtGui.QPushButton('*')
        self.tab1_general_grid.addWidget(self.tab1_general_project_btn, 0, 4)
        self.tab1_general_project_btn.setFixedWidth(30)
        # Name of output path
        self.tab1_general_outputpath_label = QtGui.QLabel('Output path')
        self.tab1_general_outputpath_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tab1_general_grid.addWidget(
            self.tab1_general_outputpath_label, 1, 2)
        self.tab1_general_outputpath_field = QtGui.QLineEdit(
            self.tab1_general_group)
        self.tab1_general_outputpath_field.setMaxLength(15)
        self.tab1_general_grid.addWidget(
            self.tab1_general_outputpath_field, 1, 3)
        self.tab1_general_outputpath_browse = QtGui.QPushButton('...')
        self.tab1_general_grid.addWidget(
            self.tab1_general_outputpath_browse, 1, 4)
        self.tab1_general_outputpath_browse.setFixedWidth(30)
        # Advanced options button
        self.tab1_advanced_btn = QtGui.QPushButton('Advanced')
        self.tab1_advanced_btn.setSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        self.tab1_general_grid.addWidget(self.tab1_advanced_btn, 0, 5, 2, 1)
        self.tab1_bottom_bar = QtGui.QHBoxLayout()
        self.tab1_grid.addLayout(self.tab1_bottom_bar, 4, 0, 1, 2)
        self.tab1_bottom_bar.addStretch(1)
        self.tab1_bottom_test = QtGui.QPushButton('Test')
        self.tab1_bottom_bar.addWidget(self.tab1_bottom_test)
        self.tab1_bottom_run = QtGui.QPushButton('Run')
        self.tab1_bottom_run.setStyleSheet('font-weight: bold;')
        self.tab1_bottom_bar.addWidget(self.tab1_bottom_run)

        ###
        # Tab 2 - Progress of the essay
        ###
        self.tab2 = QtGui.QWidget()
        self.tab2_grid = QtGui.QGridLayout(self.tab2)
        self.tabber.addTab(self.tab2, 'Job progress')

        self.tab2_table = QtGui.QTableWidget(10, 8)
        self.tab2_grid.addWidget(self.tab2_table, 0, 0, 1, 2)
        tab2_table_headers = ['Generation', 'Evaluations',
                              'Objective 1', 'Objective 2', 'Objective 3',
                              'Objective 4', 'Objective 5', 'Objective 6', ]
        self.tab2_table.setHorizontalHeaderLabels(tab2_table_headers)

        self.tab2_chart_group = QtGui.QGroupBox('Charts')
        self.tab2_chart_layout = QtGui.QHBoxLayout(self.tab2_chart_group)
        self.tab2_grid.addWidget(self.tab2_chart_group, 1, 0, 1, 2)
        self.tab2_pixmap = QtGui.QPixmap('chart.png')
        self.tab2_image = QtGui.QLabel()
        self.tab2_image.setPixmap(self.tab2_pixmap)
        self.tab2_chart_layout.addWidget(self.tab2_image)

        ###
        # Tab 3 - Detailed history
        ###
        self.tab3 = QtGui.QWidget()
        self.tab3_grid = QtGui.QGridLayout(self.tab3)
        self.tabber.addTab(self.tab3, 'Detailed history')

        # Tab 3 - Column 1 - Select individual
        self.col1 = QtGui.QVBoxLayout()
        self.tab3_grid.addLayout(self.col1, 0, 0)
        self.col1_ind_box = QtGui.QGroupBox('Individuals')
        self.col1_ind_box.setSizePolicy(QtGui.QSizePolicy.Fixed,
                                        QtGui.QSizePolicy.Preferred)
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
        self.col1_genes_table = QtGui.QTableWidget(0, 2)
        self.col1_genes_layout.addWidget(self.col1_genes_table)
        self.col1_genes_table.horizontalHeader().setStretchLastSection(True)
        self.col1_genes_table.setHorizontalHeaderLabels(['Gene', 'Allele'])
        self.col1_genes_buttons = QtGui.QHBoxLayout()
        self.col1_genes_layout.addLayout(self.col1_genes_buttons)
        self.col1_genes_express_btn = QtGui.QPushButton('(Un)express')
        self.col1_genes_buttons.addWidget(self.col1_genes_express_btn)
        self.col1_genes_express_all_btn = QtGui.QPushButton('(Un)express all')
        self.col1_genes_buttons.addWidget(self.col1_genes_express_all_btn)

        # Tab 3 - Column 2 - the environment
        self.col2 = QtGui.QVBoxLayout()
        self.tab3_grid.addLayout(self.col2, 0, 1)
        self.col2_env_box = QtGui.QGroupBox('Environment')
        self.col2_env_box.setSizePolicy(QtGui.QSizePolicy.Fixed,
                                        QtGui.QSizePolicy.Preferred)
        self.col2_env_layout = QtGui.QVBoxLayout(self.col2_env_box)
        self.col2.addWidget(self.col2_env_box)
        self.col2_env_table = QtGui.QTableWidget(0, 2)
        self.col2_env_table.horizontalHeader().setStretchLastSection(True)
        self.col2_env_table.setHorizontalHeaderLabels(['Objective', 'Score'])
        self.col2_env_layout.addWidget(self.col2_env_table)
        self.col2_env_buttons = QtGui.QHBoxLayout()
        self.col2_env_layout.addLayout(self.col2_env_buttons)
        self.col2_env_evaluate = QtGui.QPushButton('Evaluate')
        self.col2_env_buttons.addWidget(self.col2_env_evaluate)
        self.col2_env_evaluate_all = QtGui.QPushButton('Evaluate all')
        self.col2_env_buttons.addWidget(self.col2_env_evaluate_all)

        ###
        # Tab 4 - View results
        ###
        self.tab4 = QtGui.QWidget()
        self.tab4_grid = QtGui.QGridLayout(self.tab4)
        self.tabber.addTab(self.tab4, 'View results')

        self.tab4_table = QtGui.QTableWidget(30, 7)
        self.tab4_grid.addWidget(self.tab4_table, 0, 0)
        tab4_table_headers = ['Individual',
                              'Objective 1', 'Objective 2', 'Objective 3',
                              'Objective 4', 'Objective 5', 'Objective 6', ]
        self.tab4_table.setHorizontalHeaderLabels(tab4_table_headers)

        # Bottom status bar
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('GAUDInspect prototype loaded')

    def center(self):
        # get geometry of this frame (a rectangle)
        current_geometry = self.frameGeometry()
        # get center of screen
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        # move rectangle center to desktop center to guess top left location
        current_geometry.moveCenter(desktop_center)
        # move widget to the guessed top left corner
        self.move(current_geometry.topLeft())


def main():
    app = QtGui.QApplication(sys.argv)
    gaudinspectmain = GAUDInspectLiveTest()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
