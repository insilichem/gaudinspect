#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui
from . import newjob, progress, details, results


def get(parent=None):
    return GAUDInspectViewTabber(parent=parent)


class GAUDInspectViewTabber(QtGui.QTabWidget):

    def __init__(self, parent=None):
        super(GAUDInspectViewTabber, self).__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.tabs = [newjob.get(self.parent), progress.get(self.parent),
                     details.get(self.parent), results.get(self.parent)]
        for tab in self.tabs:
            self.addTab(tab, tab.title)
