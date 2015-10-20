#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GAUDInspect
===========

A full GUI for launching GAUDI jobs, analyze their progress
and examine the results.

"""

from .version import __version_info__, __version__
from PySide.QtCore import QSettings, QCoreApplication

QSettings.setDefaultFormat(QSettings.IniFormat)
QCoreApplication.setOrganizationName("GAUDI")
QCoreApplication.setApplicationName("GAUDInspect")
