#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc
from .results import GAUDInspectResultsController


class GAUDInspectController(object):

    """
    Document this!
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        # child controllers
        self.input = None
        self.progress = None
        self.details = None
        self.results = GAUDInspectResultsController(view=view)

        self.signals()

    def signals(self):
        # Viewer visibility
        self.view.tabber.currentChanged.connect(self._viewer_visibility)

    def _viewer_visibility(self, i):
        if i == 1:
            self.view.viewer.hide()
            self.view.stats.show()
        else:
            self.view.viewer.show()
            self.view.stats.hide()
