#!/usr/bin/python
# -*- coding: utf-8 -*-

from .results import GAUDInspectResultsController
from .newjob import GAUDInspectNewJobController
from .menu import GAUDInspectMenuController
from ..model.main import GAUDInspectModel


class GAUDInspectController(object):

    """
    Document this!
    """

    def __init__(self, model, view, app=None):
        self.app = app
        self.model = model
        self.view = view
        # Child controllers
        self.menu = GAUDInspectMenuController(self, view)
        self.newjob = GAUDInspectNewJobController(self, view)
        self.progress = None
        self.details = None
        self.results = GAUDInspectResultsController(self, view)

        self.signals()

    # Global signals and signals between controllers
    def signals(self):

        # Viewer visibility
        self.view.tabber.currentChanged.connect(self._viewer_visibility)

        # Drag & Drop
        self.view.fileDropped.connect(self._open_file)

        # Menu actions
        self.menu.open_file_dialog.fileSelected.connect(
            self._open_file)
        self.view.menu.results.close.triggered.connect(
            self.results.clear)

    def _viewer_visibility(self, i):
        if i == 1:
            self.view.viewer.hide()
            self.view.stats.show()
        else:
            self.view.viewer.show()
            self.view.stats.hide()

    def _open_file(self, f):
        model = GAUDInspectModel.get(f)

        if f.endswith('.out.gaudi'):
            self.results.set_model(model)
        elif f.endswith('.in.gaudi'):
            self.newjob.set_model(model)
        self.view.status('Loaded file {}'.format(f))
