#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from collections import OrderedDict

from PySide import QtGui, QtCore

from .base import GAUDInspectBaseChildController


class GAUDInspectQueueController(GAUDInspectBaseChildController):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = self.parent().menu.queue_dialog
        self.table = self.dialog.table
        self.jobs = OrderedDict()
        self.currentjob = None
        self.signals()

    def signals(self):
        self.dialog.add_job.clicked.connect(self.add_job)
        self.dialog.del_job.clicked.connect(self.del_job)
        self.dialog.del_all.clicked.connect(self.del_all)
        self.dialog.start_queue.clicked.connect(self.start_queue)
        self.dialog.stop_queue.clicked.connect(self.stop_queue)

    # Slots
    def add_job(self):
        paths, f = QtGui.QFileDialog.getOpenFileNames(
            self.dialog, 'Choose a GAUDI Input file',
            os.getcwd(), "*.in.gaudi")
        for path in paths:
            i = self.dialog.table.rowCount()
            job = GAUDInspectJobHelper(path, index=i, runner=self.parent().progress)
            path_item = QtGui.QTableWidgetItem(job.path)
            status_item = QtGui.QTableWidgetItem(job.status)
            self.jobs[path] = job

            self.table.insertRow(i)
            self.table.setItem(i, 0, path_item)
            self.table.setItem(i, 1, status_item)

    def del_job(self, i=None):
        if i is None:
            i = self.table.currentRow()
        path = self.table.item(i, 0).text()
        job = self.jobs[path]
        if job.status == job.WORKING:
            self.view.status('Cannot remove job in process')
        else:
            del self.jobs[path]
            self.table.removeRow(i)

    def del_all(self):
        for i in reversed(range(self.table.rowCount())):
            self.del_job(0)

    def set_status(self, i, status):
        self.table.item(i, 1).setText(status)

    # Queue handlers
    def start_queue(self):
        self.queue_started()
        self.process_queue()

    def process_queue(self, exit_code=None):
        pending = []
        for p, j in self.jobs.items():
            if j.status == j.PENDING:
                pending.append(j)
            elif j.status == j.WORKING:
                if exit_code:  # an error occured
                    j.status = j.FAILED
                else:  # everything went OK
                    j.status = j.FINISHED
                self.set_status(j.index, j.status)

        try:
            self.currentjob = job = pending[0]
        except IndexError:  # Queue is empty!
            self.queue_stopped()
        else:
            job.run()
            job.status = job.WORKING
            self.set_status(job.index, job.status)
            job.process.finished.connect(self.process_queue)

    def queue_started(self):
        self.enable_buttons(False)

    def queue_stopped(self):
        self.enable_buttons(True)

    def stop_queue(self):
        job = self.currentjob
        job.process.finished.disconnect(self.process_queue)
        job.process.kill()
        job.status = job.ABORTED
        self.set_status(job.index, job.status)
        self.queue_stopped()

    # Helpers
    def enable_buttons(self, value):
        buttons = [self.dialog.add_job, self.dialog.del_job, self.dialog.del_all,
                   self.dialog.start_queue]
        for btn in buttons:
            btn.setEnabled(value)


class GAUDInspectJobHelper(object):
    PENDING = 'Pending'
    WORKING = 'Running'
    FINISHED = 'Finished'
    FAILED = 'Failed'
    ABORTED = 'Aborted'

    def __init__(self, path, status=None, runner=None, index=None):
        super().__init__()
        self.path = path
        self.status = self.PENDING if status is None else status
        self.runner = runner
        self.index = index

    def run(self):
        self.process = self.runner.run(self.path)
