#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore


class GAUDInspectConfigure(QtGui.QMainWindow):

    def __init__(self):
        super(GAUDInspectConfigure, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.initUI()
        self.show()

    def initUI(self):
        # Set up main window
        self.canvas = QtGui.QWidget(self)
        self.setCentralWidget(self.canvas)
        self.layout = QtGui.QVBoxLayout(self.canvas)

        self.setWindowTitle('Configure module - GAUDInspect')
        self.setGeometry(0, 0, 300, 400)
        self.center()

        self.top_box = QtGui.QGroupBox('General settings')
        self.top_grid = QtGui.QGridLayout(self.top_box)
        self.name_label = QtGui.QLabel('Name')
        self.top_grid.addWidget(self.name_label, 0, 0)
        self.name_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.name_field = QtGui.QLineEdit()
        self.top_grid.addWidget(self.name_field, 0, 1)
        self.path_label = QtGui.QLabel('Path')
        self.top_grid.addWidget(self.path_label, 1, 0)
        self.path_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.path_field = QtGui.QLineEdit()
        self.top_grid.addWidget(self.path_field, 1, 1)
        self.layout.addWidget(self.top_box)

        # Optimization type: maximize or minimize
        self.optimization_box = QtGui.QGroupBox('Optimization')
        self.optimization_layout = QtGui.QHBoxLayout(self.optimization_box)
        self.optimization_max = QtGui.QRadioButton('Maximize')
        self.optimization_layout.addWidget(self.optimization_max)
        self.optimization_min = QtGui.QRadioButton('Minimize')
        self.optimization_layout.addWidget(self.optimization_min)
        self.optimization_layout.addStretch(1)
        self.layout.addWidget(self.optimization_box)

        # A table containing all the advanced parameters of that module
        self.parameters_box = QtGui.QGroupBox('Parameters')
        self.parameters_table = QtGui.QTableWidget(0, 2)
        self.parameters_table.setHorizontalHeaderLabels(['Parameter', 'Value'])
        self.parameters_table.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)
        self.parameters_layout = QtGui.QVBoxLayout(self.parameters_box)
        self.parameters_layout.addWidget(self.parameters_table)
        self.layout.addWidget(self.parameters_box)

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
    gaudinspectmain = GAUDInspectConfigure()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
