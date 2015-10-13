#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide.QtCore import QObject


class GAUDInspectBaseChildController(QObject):

    def __init__(self, parent=None, view=None, model=None,
                 *args, **kwargs):
        super().__init__(parent)
        self.view = view
        self.model = model

        # Optional attributes
        self.tabindex = None

    # Standard API
    def set_model(self, model):
        pass

    def signals(self):
        pass

    def slots(self):
        pass

    # Convenience methods
    def set_current(self):
        if self.tabindex is not None:
            self.view.tabber.setCurrentIndex(self.tabindex)

    def set_active(self):
        if self.tabindex is not None:
            for i in range(self.view.tabber.count()):
                self.view.tabber.setTabEnabled(i, False)
            self.view.tabber.setTabEnabled(self.tabindex, True)
            self.view.tabber.setCurrentIndex(self.tabindex)

    def restore_enabled(self):
        for i in range(self.view.tabber.count()):
            self.view.tabber.setTabEnabled(i, True)
