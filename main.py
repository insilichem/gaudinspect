#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from controller.main import GAUDInspectController
from model.main import GAUDInspectModel
from view.main import GAUDInspectView


def main():
    try:
        app = QtGui.QApplication(sys.argv)
    except RuntimeError:
        app = QtGui.QApplication.instance()

    model, view = GAUDInspectModel(sys.argv[1]), GAUDInspectView()
    controller = GAUDInspectController(model, view)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
