#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PySide.QtGui import QFileDialog, QAction


def get(parent=None):
    return GAUDInspectViewTopMenu(parent=parent)


class GAUDInspectViewTopMenu(object):

    def __init__(self, parent=None):
        self.parent = parent

        self.dialogs()
        self.initUI()

    def initUI(self):
        # Top menu - File
        self.parent.menu_file = self.parent.menuBar().addMenu("&File")
        self.parent.menu_file.addAction('New')
        self.parent.menu_file.addAction('Open', self.open_file_dialog.open)
        self.parent.menu_file.addAction('Save')
        self.parent.menu_file.addSeparator()
        self.parent.menu_file.addAction('Import state')
        self.parent.menu_file.addAction('Export state')
        self.parent.menu_file.addSeparator()
        self.parent.menu_file.addAction('Exit')

        # Top menu - Edit
        self.parent.menu_edit = self.parent.menuBar().addMenu("&Edit")
        self.parent.menu_edit.addAction('Project settings')
        self.parent.menu_edit.addAction('Project file (advanced)')
        self.parent.menu_edit.addSeparator()
        self.parent.menu_edit.addAction('Configuration')

        # Top menu - Viewer
        self.parent.menu_viewer = self.parent.menuBar().addMenu("&Viewer")
        self.parent.menu_viewer.addAction('Enable effects',
                                          self.parent.viewer.enable_effects)
        self.parent.menu_viewer.addAction('Disable effects',
                                          self.parent.viewer.disable_effects)
        self.parent.menu_viewer.addSeparator()
        self.parent.menu_viewer.addAction('Configuration')

        # Top menu - Controls
        self.parent.menu_controls = self.parent.menuBar().addMenu("&Controls")
        self.parent.menu_controls.addAction('Run')
        self.parent.menu_controls.addAction('Finish')
        self.parent.menu_controls.addAction('Cancel')
        self.parent.menu_controls.addSeparator()
        self.parent.menu_controls.addAction('Pause')
        self.parent.menu_controls.addAction('Pause at next generation')
        self.parent.menu_controls.addAction('Forward one generation')
        self.parent.menu_controls.addSeparator()
        self.parent.menu_controls.addAction('Show live stats')

        # Top menu - Controls
        self.parent.menu_results = self.parent.menuBar().addMenu("&Results")
        self.action_close_results = QAction('Close results', self.parent)
        self.parent.menu_results.addAction(self.action_close_results)

        # Top menu - Help
        self.parent.menu_help = self.parent.menuBar().addMenu("&Help")
        self.parent.menu_help.addAction('Help')
        self.parent.menu_help.addAction('Website')
        self.parent.menu_help.addSeparator()
        self.parent.menu_help.addAction('About')

    # Dialogs
    def dialogs(self):
        self.open_file_dialog = QFileDialog(self.parent, "Open GAUDI file", os.getcwd(),
                                            "GAUDI output (*.out.gaudi);; GAUDI input (*.in.gaudi)")
        self.open_file_dialog.setFileMode(QFileDialog.ExistingFile)
