#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from gaudinspect.controller.main import GAUDInspectController
from gaudinspect.model.main import GAUDInspectModel
from gaudinspect.view.main import GAUDInspectView


def main():
    try:
        app = QtGui.QApplication(sys.argv)
    except RuntimeError:
        app = QtGui.QApplication.instance()

    model, view = GAUDInspectModel(), GAUDInspectView()
    controller = GAUDInspectController(model, view)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
