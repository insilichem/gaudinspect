#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide.QtCore import Qt
from ...version import __version__, __author__, __copyright__
from ..resources import images

aboutmsg = """
<h1>GAUDInspect</h1>
<i>A GUI for GAUDIasm</i><br />
<p width="250">
    Version: {}<br />
    Authors: {}<br />
    Copyright: {}
</p>
""".format(__version__, __author__, __copyright__)


class GAUDInspectAboutDialog(QtGui.QDialog):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent)
        self.setWindowTitle("About GAUDInspect")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.initUI()

    def initUI(self):
        self.layout = QtGui.QGridLayout(self)

        self.logo = QtGui.QLabel(self)
        self.logo.setPixmap(QtGui.QPixmap(":/logo.png"))
        self.layout.addWidget(self.logo, 0, 0)

        self.aboutmsg = QtGui.QLabel(aboutmsg)
        self.aboutmsg.setWordWrap(True)
        self.aboutmsg.setMaximumWidth(250)
        self.layout.addWidget(self.aboutmsg, 0, 1)
        # The logo has some margins. Add some to the text too
        margins = self.aboutmsg.contentsMargins()
        margins.setRight(margins.right() + 10)
        self.aboutmsg.setContentsMargins(margins)

    def showEvent(self, event):
        super().showEvent(event)
        self.adjustSize()
        self.setFixedSize(self.size())
