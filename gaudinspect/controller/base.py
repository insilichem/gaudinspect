#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module provides base classes that all controllers must inherit.

"""

from __future__ import print_function, division, absolute_import
from PyQt4.QtCore import QObject


class GAUDInspectBaseChildController(QObject):

    """
    A base class that child controllers must inherit to be functional.

    Child controllers are those who will be called by `.main.GAUDInspectController`
    and are devoted to handle specific parts of the application.

    Parameters
    ----------
    parent : QObject
        Most of the time, it will be the main instance of
        `.main.GAUDInspectController`, declared along the
        master view and model in the root `main.py`.
        Needed to handle the parent mechanism of Qt.

    tabindex : int, optional
        If the controller handles a `QWidget` that is part of a `QTabWidget`, this
        attribute keeps the tab index in the tabber. That way, some helper
        methods can be defined.

    Attributes
    ----------
    app : PyQt4.QtGui.QApplication
        Shortcut to the QApplication instance that runs all the GUI.
    view : PyQt4.QtGui.QMainWindow
        The main view of the application, extracted directly from the parent
        controller.
    model : object
        The main model of the application, extracted directly from the parent
        controller.

    """

    def __init__(self, parent=None, tabindex=None, *args, **kwargs):
        super(GAUDInspectBaseChildController, self).__init__(parent)
        self.app = self.parent().app
        self.view = self.parent().view
        self.model = self.parent().model
        # Optional attributes
        self.tabindex = None
        self.childmodel = None

    # Standard API
    def set_model(self, model):
        """
        Sets child model if it was not declared at instance initialization.
        """
        pass

    def signals(self):
        """
        Connects all signals to their respective slots. To be called
        from `__init__`, if needed.
        """
        pass

    def slots(self):
        """
        Since a slot can consist of new objects that are created
        on demand with private methods, this method groups them
        together with more friendly names.
        """
        pass

    # Convenience methods
    def set_current(self):
        """
        If `self.tabindex` is defined, set the focus to that tab.
        """
        if self.tabindex is not None:
            self.view.tabber.setCurrentIndex(self.tabindex)

    def set_active(self):
        """
        If `self.tabindex` is defined, set the focus to that tab
        and disable any other visible tabs.
        """
        if self.tabindex is not None:
            for i in range(self.view.tabber.count()):
                self.view.tabber.setTabEnabled(i, False)
            self.view.tabber.setTabEnabled(self.tabindex, True)
            self.view.tabber.setCurrentIndex(self.tabindex)

    def restore_enabled(self):
        """
        Reenable all tabs.
        """
        for i in range(self.view.tabber.count()):
            self.view.tabber.setTabEnabled(i, True)
