#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc
from .results import GAUDInspectResultsController
from ..model.main import GAUDInspectModel


class GAUDInspectController(object):

    """
    Document this!
    """

    def __init__(self, model, view, app=None):
        self.app = None
        self.model = model
        self.view = view

        # Child controllers
        self.input = None
        self.progress = None
        self.details = None
        self.results = GAUDInspectResultsController(view=view)

        self.signals()

    def signals(self):
        # Viewer visibility
        self.view.tabber.currentChanged.connect(self._viewer_visibility)
        self.view.fileDropped.connect(self._open_file)

        # Results signals
        self.view.menu.open_file_dialog.fileSelected.connect(
            self._open_file)
        self.view.menu.action_close_results.triggered.connect(
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
        # elif f.endswith('.in.gaudi'):
        #     pass
        # self.input.load_model(model)
