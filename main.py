#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The main launcher of the GUI app. It does nothing fancy, except
loading the settings for all the application and calling the
main controller, model and view.

"""

import sys
from PySide.QtGui import QApplication
from PySide.QtCore import QSettings, QCoreApplication
from gaudinspect.controller.main import GAUDInspectController
from gaudinspect.model.main import GAUDInspectModel
from gaudinspect.view.main import GAUDInspectView


def main():
    try:
        app = QApplication(sys.argv)
    except RuntimeError:
        app = QApplication.instance()

    QSettings.setDefaultFormat(QSettings.IniFormat)
    QCoreApplication.setOrganizationName("GAUDI")
    QCoreApplication.setApplicationName("GAUDInspect")
    app.settings = QSettings()

    model, view = GAUDInspectModel(app=app), GAUDInspectView(app=app)
    controller = GAUDInspectController(model, view, app=app)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
