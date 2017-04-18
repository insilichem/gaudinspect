#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import


"""
The main launcher of the GUI app. It does nothing fancy, except
loading the settings for all the application and calling the
main controller, model and view.

"""

import sys

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QSettings
from gaudinspect.controller.main import GAUDInspectController
from gaudinspect.model.main import GAUDInspectModel
from gaudinspect.view.main import GAUDInspectView


def main():
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)

    app.settings = QSettings()

    model, view = GAUDInspectModel(app=app), GAUDInspectView(app=app)
    controller = GAUDInspectController(model, view, app=app)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
