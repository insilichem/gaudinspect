#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore, QtOpenGL
from . import viewer, menu, tabber, stats
from .resources import images


class GAUDInspectView(QtGui.QMainWindow):

    fileDropped = QtCore.Signal(str)

    def __init__(self, app=None):
        super(GAUDInspectView, self).__init__()
        self.app = app
        self.setWindowIcon(QtGui.QIcon(':/logo.png'))
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
        self._center()

        # Main layout
        self.left = QtGui.QWidget()
        self.viewer = viewer.get(self.glcontext, self)
        self.stats = stats.get()
        self.tabber = tabber.get()
        self.statusbar = self.statusBar()
        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.menu = menu.get(self)

        # Organize widgets
        self.layout.addWidget(self.splitter, 0, 0)
        self.left_layout = QtGui.QGridLayout(self.left)
        self.left_layout.addWidget(self.viewer, 0, 0)
        self.left_layout.addWidget(self.stats, 0, 0)

        self.splitter.addWidget(self.left)
        self.splitter.addWidget(self.tabber)
        self.left_layout.setContentsMargins(0, 0, 0, 0)

    def _center(self):
        # get geometry of this frame (a rectangle)
        current_geometry = self.frameGeometry()
        # get center of screen
        desktop_center = QtGui.QDesktopWidget().availableGeometry().center()
        # move rectangle center to desktop center to guess top left location
        current_geometry.moveCenter(desktop_center)
        # move widget to the guessed top left corner
        self.move(current_geometry.topLeft())

    # Implement drag&drop
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls() and \
                next(str(url.toLocalFile()) for url in e.mimeData().urls()).endswith('.gaudi'):
            e.accept()
            self.setWindowOpacity(0.8)
        else:
            e.ignore()

    def dragLeaveEvent(self, e):
        self.setWindowOpacity(1.0)

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            p = next(str(url.toLocalFile()) for url in e.mimeData().urls())
            self.fileDropped.emit(p)
            self.setWindowOpacity(1.0)
        else:
            e.ignore()

    # Status bar handler
    def status(self, txt):
        self.statusbar.showMessage(txt, 3000)
