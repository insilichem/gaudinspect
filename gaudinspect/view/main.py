#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore, QtOpenGL
from PySide.QtCore import Signal
from . import viewer, topmenu, tabber, stats


class GAUDInspectView(QtGui.QMainWindow):

    fileDropped = Signal(str)

    def __init__(self):
        super(GAUDInspectView, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.glcontext = QtOpenGL.QGLContext(QtOpenGL.QGLFormat())
        self.setAcceptDrops(True)

        self.initUI()
        self.show()

    def initUI(self):
        # Set up main window
        self.canvas = QtGui.QWidget(self)
        self.canvas.setObjectName("MainCanvas")
        self.setCentralWidget(self.canvas)
        self.layout = QtGui.QGridLayout(self.canvas)

        self.setWindowTitle('GAUDInspect')
        self.setGeometry(0, 0, 900, 600)
        self.center()

        # Main layout
        self.left = QtGui.QWidget()
        self.viewer = viewer.get(self.glcontext, self)
        self.stats = stats.get(self)
        self.tabber = tabber.get(self)
        self.statusbar = self.statusBar()
        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.menu = topmenu.get(self)

        # Organize widgets
        self.layout.addWidget(self.splitter, 0, 0)
        self.left_layout = QtGui.QGridLayout(self.left)
        self.left_layout.addWidget(self.viewer, 0, 0)
        self.left_layout.addWidget(self.stats, 0, 0)

        self.splitter.addWidget(self.left)
        self.splitter.addWidget(self.tabber)
        self.left_layout.setContentsMargins(0, 0, 0, 0)

    def center(self):
        # get geometry of this frame (a rectangle)
        current_geometry = self.frameGeometry()
        # get center of screen
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        # move rectangle center to desktop center to guess top left location
        current_geometry.moveCenter(desktop_center)
        # move widget to the guessed top left corner
        self.move(current_geometry.topLeft())

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            p = next(str(url.toLocalFile()) for url in e.mimeData().urls())
            self.fileDropped.emit(p)
        else:
            e.ignore()
