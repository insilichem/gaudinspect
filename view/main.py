#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore, QtOpenGL
from . import viewer, topmenu, tabber


class GAUDInspectView(QtGui.QMainWindow):

    def __init__(self):
        super(GAUDInspectView, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.glcontext = QtOpenGL.QGLContext(QtOpenGL.QGLFormat())

        self.initUI()
        self.show()

    def initUI(self):
        # Set up main window
        self.canvas = QtGui.QWidget(self)
        self.setCentralWidget(self.canvas)
        self.layout = QtGui.QGridLayout(self.canvas)

        self.setWindowTitle('GAUDInspect')
        self.setGeometry(0, 0, 900, 600)
        self.center()

        # Main layout
        self.menu = topmenu.get(self)
        self.viewer = viewer.get(self.glcontext, self)
        self.tabber = tabber.get(self)
        self.statusbar = self.statusBar()
        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

        # Organize widgets
        self.layout.addWidget(self.splitter, 0, 0)
        self.splitter.addWidget(self.viewer)
        self.splitter.addWidget(self.tabber)

    def center(self):
        # get geometry of this frame (a rectangle)
        current_geometry = self.frameGeometry()
        # get center of screen
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        # move rectangle center to desktop center to guess top left location
        current_geometry.moveCenter(desktop_center)
        # move widget to the guessed top left corner
        self.move(current_geometry.topLeft())
