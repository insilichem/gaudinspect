#!/usr/bin/python
# -*- coding: utf-8 -*-


def get(parent=None):
    return GAUDInspectViewTopMenu(parent=parent)


class GAUDInspectViewTopMenu(object):

    def __init__(self, parent=None):
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Top menu - File
        self.parent.menu_file = self.parent.menuBar().addMenu("&File")
        self.parent.menu_file.addAction('New')
        self.parent.menu_file.addAction('Open')
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

        # Top menu - Help
        self.parent.menu_help = self.parent.menuBar().addMenu("&Help")
        self.parent.menu_help.addAction('Help')
        self.parent.menu_help.addAction('Website')
        self.parent.menu_help.addSeparator()
        self.parent.menu_help.addAction('About')
