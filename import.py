#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui


class GAUDInspectImportPopulation(QtGui.QMainWindow):

    def __init__(self):
        super(GAUDInspectImportPopulation, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.initUI()
        self.show()

    def initUI(self):
        # Set up main window
        self.canvas = QtGui.QWidget(self)
        self.setCentralWidget(self.canvas)
        self.layout = QtGui.QVBoxLayout(self.canvas)

        self.setWindowTitle('Import population - GAUDInspect')
        self.center()

        warning = QtGui.QLabel(
            'Note: All previous settings will be overriden!')
        self.layout.addWidget(warning)

        self.box = QtGui.QGroupBox('Select population file')
        self.layout.addWidget(self.box)
        self.box_layout = QtGui.QHBoxLayout(self.box)
        self.path_field = QtGui.QLineEdit()
        self.box_layout.addWidget(self.path_field)
        self.path_btn = QtGui.QPushButton('...')
        self.path_btn.setFixedWidth(30)
        self.box_layout.addWidget(self.path_btn)

        self.bottom_buttons = QtGui.QHBoxLayout()
        self.layout.addLayout(self.bottom_buttons)
        self.bottom_buttons.addStretch(1)
        self.ok_btn = QtGui.QPushButton('OK')
        self.bottom_buttons.addWidget(self.ok_btn)
        self.cancel_btn = QtGui.QPushButton('Cancel')
        self.bottom_buttons.addWidget(self.cancel_btn)

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
    gaudinspectmain = GAUDInspectImportPopulation()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
