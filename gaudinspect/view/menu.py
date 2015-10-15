#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide.QtGui import QAction, QMenu


def get(parent=None):
    return GAUDInspectViewMenu(parent=parent)


class GAUDInspectViewMenu(object):

    def __init__(self, parent=None):
        self.parent = parent
        self.initUI()
        self._gray_out()

    def initUI(self):
        # Top menu - File
        self.file = self.parent.menuBar().addMenu("&File")
        self.file.new = QAction('New', self.file)
        self.file.addAction(self.file.new)
        self.file.open = QAction('Open', self.file)
        self.file.addAction(self.file.open)
        self.file.open_recent = QMenu("Open recent...")
        self.file.addMenu(self.file.open_recent)
        self.file.save = QAction('Save', self.file)
        self.file.addAction(self.file.save)

        self.file.addSeparator()

        self.file.import_state = QAction('Import state', self.file)
        self.file.addAction(self.file.import_state)
        self.file.export_state = QAction('Export state', self.file)
        self.file.addAction(self.file.export_state)
        self.file.addSeparator()
        self.file.exit = QAction('Exit', self.file)
        self.file.addAction(self.file.exit)

        # Top menu - Edit
        self.edit = self.parent.menuBar().addMenu("&Edit")
        self.edit.project_settings = QAction('Project settings', self.edit)
        self.edit.addAction(self.edit.project_settings)
        self.edit.project_advanced = QAction(
            'Project file (advanced)', self.edit)
        self.edit.addAction(self.edit.project_advanced)
        self.edit.addSeparator()
        self.edit.configuration = QAction('Configuration', self.edit)
        self.edit.addAction(self.edit.configuration)

        # Top menu - Viewer
        self.viewer = self.parent.menuBar().addMenu("&Viewer")
        self.viewer.enable_fx = QAction('Enable effects', self.viewer)
        self.viewer.addAction(self.viewer.enable_fx)
        self.viewer.disable_fx = QAction('Disable effects', self.viewer)
        self.viewer.addAction(self.viewer.disable_fx)
        self.viewer.addSeparator()
        self.viewer.configuration = QAction('Configuration', self.viewer)
        self.viewer.addAction(self.viewer.configuration)

        # Top menu - Controls
        self.controls = self.parent.menuBar().addMenu("&Controls")
        self.controls.run = QAction('Run', self.controls)
        self.controls.addAction(self.controls.run)
        self.controls.finish = QAction('Finish', self.controls)
        self.controls.addAction(self.controls.finish)
        self.controls.cancel = QAction('Cancel', self.controls)
        self.controls.addAction(self.controls.cancel)
        self.controls.addSeparator()
        self.controls.pause = QAction('Pause', self.controls)
        self.controls.addAction(self.controls.pause)
        self.controls.pause_next = QAction(
            'Pause at next generation', self.controls)
        self.controls.addAction(self.controls.pause_next)
        self.controls.forward = QAction(
            'Forward one generation', self.controls)
        self.controls.addAction(self.controls.forward)
        self.controls.addSeparator()
        self.controls.live_stats = QAction('Show live stats', self.controls)
        self.controls.addAction(self.controls.live_stats)

        # Top menu - Controls
        self.results = self.parent.menuBar().addMenu("&Results")
        self.results.close = QAction('Close results', self.results)
        self.results.addAction(self.results.close)

        # Top menu - Help
        self.help = self.parent.menuBar().addMenu("&Help")
        self.help.help = QAction('Help', self.help)
        self.help.addAction(self.help.help)
        self.help.website = QAction('Website', self.help)
        self.help.addAction(self.help.website)
        self.help.addSeparator()
        self.help.about = QAction('About', self.help)
        self.help.addAction(self.help.about)

    def _gray_out(self):
        items = [
            self.file.new,
            self.file.import_state,
            self.file.export_state,
            self.edit.project_settings,
            self.edit.project_advanced,
            self.viewer.configuration,
            self.controls.run,
            self.controls.finish,
            self.controls.cancel,
            self.controls.pause,
            self.controls.pause_next,
            self.controls.forward,
            self.controls.live_stats,
            self.help.help,
            self.help.website
        ]
        for item in items:
            item.setEnabled(False)
