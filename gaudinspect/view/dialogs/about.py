#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui
from ...version import __version__, __author__, __copyright__

aboutmsg = """
<h1>GAUDInspect</h1>
<i>A GUI for GAUDIasm</i><br />
<p>
    Version: {}<br />
    Authors: {}<br />
    Copyright: {}
</p>
""".format(__version__, __author__, __copyright__)


class GAUDInspectAboutDialog(QtGui.QDialog):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self.setWindowTitle("About GAUDInspect")
        self.initUI()

    def initUI(self):
        self.canvas = QtGui.QWidget(self)
        self.layout = QtGui.QGridLayout(self.canvas)

        self.logo = QtGui.QLabel(self)
        self.logo.setPixmap(QtGui.QPixmap("icon.png"))

        self.layout.addWidget(self.logo, 0, 0)

        self.aboutmsg = QtGui.QLabel(aboutmsg)
        margins = self.aboutmsg.contentsMargins()
        margins.setRight(margins.right() + 10)
        self.aboutmsg.setContentsMargins(margins)
        self.layout.addWidget(self.aboutmsg, 0, 1)

    def showEvent(self, event):
        super().showEvent(event)
        self.adjustSize()
