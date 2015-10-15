#!/usr/bin/python
# -*- coding: utf-8 -*-

from .results import GAUDInspectResultsController
from .newjob import GAUDInspectNewJobController
from .menu import GAUDInspectMenuController
from .progress import GAUDInspectProgressController
from ..model.main import GAUDInspectModel
from .. import configuration

from PySide import QtGui, QtCore


class GAUDInspectController(QtCore.QObject):

    """
    Document this!
    """

    def __init__(self, model, view, app=None):
        super().__init__(app)
        self.app = app
        self.model = model
        self.view = view
        # Child controllers
        self.menu = GAUDInspectMenuController(parent=self, view=view,
                                              recent_model=self.model.recent)
        self.newjob = GAUDInspectNewJobController(parent=self, view=view)
        self.progress = GAUDInspectProgressController(parent=self, view=view,
                                                      recent_model=self.model.recent.input_only)
        self.details = None
        self.results = GAUDInspectResultsController(parent=self, view=view)
        # Start things up
        self._settings()
        self._signals()
        self._check_firstrun()

    # API
    def open_file(self, f, temporary=False):
        model = GAUDInspectModel.get(f)

        if f.endswith('.out.gaudi'):
            self.results.set_model(model)
        elif f.endswith('.in.gaudi'):
            self.newjob.set_model(model)
            self.progress.tab.input_fld.setEditText(f)
        self.view.status('Loaded file {}'.format(f))

        if not temporary:
            self.model.recent.add_entry(f, sync=True, check_uniqueness=True)

    # Private methods
    def _settings(self):
        configured = self.app.settings.value("flags/configured")
        if not configured:
            settings = QtCore.QSettings()
            for key, val in configuration.default.items():
                settings.setValue(key, val)

    def _check_firstrun(self):
        configured = self.app.settings.value("flags/configured")
        path = self.app.settings.value("paths/gaudi")

        if not configured or not path:
            self._configure_msg()

    # Global signals and signals between controllers
    def _signals(self):
        # Viewer visibility
        self.view.tabber.currentChanged.connect(self._viewer_visibility)

        # Drag & Drop
        self.view.fileDropped.connect(self.open_file)

        # Menu actions
        self.menu.open_file_dialog.fileSelected.connect(
            self.open_file)
        self.view.menu.results.close.triggered.connect(
            self.results.clear)

    def _viewer_visibility(self, i):
        if i == 1:
            self.view.viewer.hide()
            self.view.stats.show()
        else:
            self.view.viewer.show()
            self.view.stats.hide()

    def _configure_msg(self):
        msg = """GAUDInspect needs some configuration before you can use it.
Go to Edit - Configuration to fill in the details."""
        returned = QtGui.QMessageBox.information(
            self.view, "GAUDInspect Configuration",
            msg, QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ignore)
        if returned == QtGui.QMessageBox.Ok:
            self.menu._configure()
