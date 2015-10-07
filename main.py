#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from PySide import QtGui, QtCore
from gaudinspect.controller.main import GAUDInspectController
from gaudinspect.model.main import GAUDInspectModel
from gaudinspect.view.main import GAUDInspectView


def main():
    try:
        app = QtGui.QApplication(sys.argv)
    except RuntimeError:
        app = QtGui.QApplication.instance()

    app.settings = QtCore.QSettings("GAUDI", "GAUDInspect")
    model, view = GAUDInspectModel(app=app), GAUDInspectView(app=app)
    controller = GAUDInspectController(model, view, app=app)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
