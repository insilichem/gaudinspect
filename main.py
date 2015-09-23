#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui, QtCore
from gaudinspect.controller.main import GAUDInspectController
from gaudinspect.model.main import GAUDInspectModel
from gaudinspect.view.main import GAUDInspectView


def main():
    sys.path.append('C:/Users/Jaime/dev/gaudi')
    try:
        app = QtGui.QApplication(sys.argv)
    except RuntimeError:
        app = QtGui.QApplication.instance()

    app.settings = QtCore.QSettings("GAUDI", "GAUDInspect")
    app.settings.setValue(
        "general/gaudipath", "C:/Users/Jaime/dev/gaudi/gaudi")
    model, view = GAUDInspectModel(app=app), GAUDInspectView(app=app)
    controller = GAUDInspectController(model, view, app=app)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
