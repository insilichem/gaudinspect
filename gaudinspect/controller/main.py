#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from .results import GAUDInspectResultsController
from .newjob import GAUDInspectNewJobController
from .menu import GAUDInspectMenuController
from .progress import GAUDInspectProgressController
from .queue import GAUDInspectQueueController
from ..model.main import GAUDInspectModel

from .. import configuration

from PyQt4 import QtGui, QtCore


class GAUDInspectController(QtCore.QObject):

    """
    This class is the main controller of all the application.

    Parameters
    ----------
    app : PyQt4.QtGui.QApplication
        The QApplication instance that runs all the GUI.
    model : ..model.main.GAUDInspectModel
        The main model of the application, the only instance of
        `..model.main.GAUDInspectModel`.
    view : ..view.main.GAUDInspectView
        The main view of the application, the only instance of
        `..view.main.GAUDInspectView`.

    Attributes
    ----------
    menu : menu.GAUDInspectMenuController
        The child controller that handles the menu bar view and actions.

    newjob : newjob.GAUDInspectNewJobController
        The child controller that handles the creation of new jobs.

    progress : progress.GAUDInspectProgressController
        The child controller that handles the progress reporting of running jobs.

    details : None
        This part is not implemented yet.

    results : results.GAUDInspectResultsController
        The child controller that handles the visualization of output files and results.

    queue : queue.GAUDInspectQueueController
        The child controller that handles the queue system in batch jobs.

    """

    def __init__(self, model, view, app=None):
        super(GAUDInspectController, self).__init__(app)
        self.app = app
        self.model = model
        self.view = view
        # Child controllers
        self.menu = GAUDInspectMenuController(parent=self,
                                              recent_model=self.model.recent)
        self.newjob = GAUDInspectNewJobController(parent=self)
        self.progress = GAUDInspectProgressController(parent=self,
                                                      recent_model=self.model.recent.input_only)
        self.details = None
        self.results = GAUDInspectResultsController(parent=self)
        self.queue = GAUDInspectQueueController(parent=self)

        # Start things up
        self._check_defaults()
        self._signals()
        self._check_configuration()

    # API
    def open_file(self, path, temporary=False):
        """
        Retrieves the correct submodel from `GAUDInspectModel` and
        delivers it to the appropiate child controller.

        Parameters
        ----------
        path : str
            The path to the file being opened by `GAUDInspectModel.get`.

        temporary : bool, optional
            If `True`, don't add the path to the recent files history.

        """
        model = GAUDInspectModel.get(path)

        if path.endswith('.gaudi-output'):
            self.results.set_model(model)
        elif path.endswith('.gaudi-input'):
            self.newjob.set_model(model)
            self.progress.tab.input_fld.setEditText(path)
        self.view.status('Loaded file {}'.format(path))

        if not temporary:
            self.model.recent.add_entry(path, sync=True, check_uniqueness=True)

    # Private methods
    def _check_defaults(self):
        """
        Check if default configuration is loaded or not. If not,
        load default values.
        """
        settings = QtCore.QSettings()
        if not settings.value("flags/configured"):
            for key, val in configuration.default.items():
                settings.setValue(key, val)

    def _check_configuration(self):
        """
        The default configuration needes user input, so it checks
        if the needed configuration is met and displays a warning
        message if it is not.
        """
        configured = self.app.settings.value("flags/configured")
        path = self.app.settings.value("paths/gaudi")

        if not configured or not path:
            self._configuration_needed_warning()

    # Global signals and signals between controllers
    def _signals(self):
        """
        Connect signals and slots
        """
        # Viewer visibility
        self.view.tabber.currentChanged.connect(self._viewer_visibility)

        # Drag & Drop
        self.view.fileDropped.connect(self.open_file)

        # Menu actions
        self.menu.open_file_dialog.fileSelected.connect(
            self.open_file)
        self.view.menu.results.close.triggered.connect(
            self.results.clear)

    # Slots
    def _viewer_visibility(self, i):
        """
        A slot that hides or shows the molecular viewer according to
        the current index of the tabber widget.

        Parameters
        ----------
        i : int
            The index corresponding to the active tab, as passed
            by the `Pyside.QtGui.QTabWidget.currentChanged` signal.
        """
        if i == 1:
            self.view.viewer.hide()
            self.view.stats.show()
        else:
            self.view.viewer.show()
            self.view.stats.hide()

    def _configuration_needed_warning(self):
        """
        The warning message that is displayed if the configuration
        has not been completed. Called by `self._check_firstrun`.
        """
        msg = """GAUDInspect needs some configuration before you can use it.
Go to Edit - Configuration to fill in the details."""
        returned = QtGui.QMessageBox.information(
            self.view, "GAUDInspect Configuration",
            msg, QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ignore)
        if returned == QtGui.QMessageBox.Ok:
            self.menu.configure_dialog()
