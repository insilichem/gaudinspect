#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore


class GAUDInspectSelectModule(QtGui.QMainWindow):

    def __init__(self):
        super(GAUDInspectSelectModule, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.initUI()
        self.show()

    def initUI(self):
        # Set up main window
        self.canvas = QtGui.QWidget(self)
        self.setCentralWidget(self.canvas)
        self.setWindowTitle('Select Module - GAUDInspect')
        self.layout = QtGui.QVBoxLayout(self.canvas)
        self.setGeometry(0, 0, 400, 250)
        self.center()

        # Draw GUI
        # Select path dialog
        self.path_box = QtGui.QGroupBox('Select modules path')
        self.path_box.setSizePolicy(QtGui.QSizePolicy.Preferred,
                                    QtGui.QSizePolicy.Fixed)
        self.layout.addWidget(self.path_box)
        self.path_layout = QtGui.QHBoxLayout()
        self.path_box.setLayout(self.path_layout)
        self.path_field = QtGui.QLineEdit()
        self.path_btn = QtGui.QPushButton('...')
        self.path_layout.addWidget(self.path_field)
        self.path_layout.addWidget(self.path_btn)

        # Choose a module
        self.choose_box = QtGui.QGroupBox('Choose a module')
        self.layout.addWidget(self.choose_box)
        self.choose_layout = QtGui.QGridLayout()
        self.choose_box.setLayout(self.choose_layout)
        # List of modules
        self.choose_list = QtGui.QListWidget()
        self.choose_layout.addWidget(self.choose_list, 0, 0, 3, 1)
        # Actions buttons
        self.choose_add_btn = QtGui.QPushButton('Add')
        self.choose_info_btn = QtGui.QPushButton('Info')
        self.choose_layout.addWidget(self.choose_add_btn, 0, 1)
        self.choose_layout.addWidget(self.choose_info_btn, 1, 1)

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
    gaudinspectmain = GAUDInspectSelectModule()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
