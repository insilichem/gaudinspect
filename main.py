#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from view.main import GAUDInspectView


def main():
    app = QtGui.QApplication(sys.argv)
    app_view = GAUDInspectView()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
