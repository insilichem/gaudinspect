#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui
from .tabs import newjob, progress, details, results


def get():
    return GAUDInspectViewTabber()


class GAUDInspectViewTabber(QtGui.QTabWidget):

    def __init__(self):
        super(GAUDInspectViewTabber, self).__init__()
        # self.parent = parent
        self.initUI()

    def initUI(self):
        self.tabs = [newjob.get(), progress.get(),
                     details.get(), results.get()]
        for tab in self.tabs:
            self.addTab(tab, tab.title)
