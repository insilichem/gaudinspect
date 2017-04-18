#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import


"""
GAUDInspect
===========

A full GUI for launching GAUDI jobs, analyze their progress
and examine the results.

"""

from .version import __version_info__, __version__  # noqa
import sip
sip.setapi(u'QDate', 2)
sip.setapi(u'QDateTime', 2)
sip.setapi(u'QString', 2)
sip.setapi(u'QTextStream', 2)
sip.setapi(u'QTime', 2)
sip.setapi(u'QUrl', 2)
sip.setapi(u'QVariant', 2)

from PyQt4.QtCore import QSettings, QCoreApplication

QSettings.setDefaultFormat(QSettings.IniFormat)
QCoreApplication.setOrganizationName("GAUDI")
QCoreApplication.setApplicationName("GAUDInspect")
