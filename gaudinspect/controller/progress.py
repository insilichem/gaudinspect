#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import
import os
import yaml

from PyQt4 import QtCore, QtGui

from .base import GAUDInspectBaseChildController


class GAUDInspectProgressController(GAUDInspectBaseChildController):

    def __init__(self, recent_model=None, **kwargs):
        super(GAUDInspectProgressController, self).__init__(**kwargs)
        self.tabindex = 1
        self.tab = self.view.tabber.tabs[self.tabindex]
        self.recent = recent_model
        if self.recent:
            self.tab.input_fld.setModel(self.recent)
            self.tab.input_fld.setCurrentIndex(-1)
        self.process = None
        self.history = []
        self.inputfile = {}
        self.signals()

    def signals(self):
        self.parent().newjob.file_ready.connect(self.run)
        self.tab.input_fld.activated.connect(
            self.open_file_from_dropdown)
        self.tab.input_btn.clicked.connect(self.open_file)
        self.tab.input_run.clicked.connect(self.run)

    def connect_process_signals(self):
        self.process.readyReadStandardOutput.connect(self.report)
        self.process.started.connect(self.process_started)
        self.process.finished.connect(self.process_finished)

    def run(self, path=None):

        if path is None:
            path = self.tab.input_fld.currentText()
        else:
            self.tab.input_fld.setEditText(path)

        # settings = QtCore.QSettings()
        # chimera = settings.value("paths/chimera")
        # gaudi = os.path.join(settings.value("paths/gaudi"), "launch.py")
        # args = ['--debug', '--nogui', '--silent', '--script',
        #         "{} {}".format(gaudi, path)]

        exe = "gaudi"
        args = ['run', path]
        print("Running", path)
        self.process = QtCore.QProcess(self.view)
        self.connect_process_signals()
        self.process.start(exe, args)

        return self.process

    def report(self):
        # Raw output
        line = str(self.process.readAllStandardOutput())
        print(line)
        self.tab.textbox.append(line)
        # Tabulated data
        self.add_row(*self.parse_output(line))

    @staticmethod  # The 'Model' in output parsing
    def parse_output(line):
        try:
            int(line.strip()[0])
        except (IndexError, ValueError):
            # IndexError means that line is empty
            # ValueError indicates it's not a number
            return [None] * 3
        else:
            gen, evals, avg, min_, max_ = line.strip().split('\t')
            gen, evals = [int(x.strip()) for x in (gen, evals)]
            objectives = list(zip(*(list(map(float, x.strip('[] ').split()))
                                    for x in (avg, min_, max_))))
            return gen, evals, objectives

    # The 'Controller' of output parsing
    def add_row(self, gen, evals, objectives):
        if gen is not None:
            self.history.append((evals, objectives))
            self.tab.progressbar.setValue(gen)
            i = self.tab.table.rowCount()
            self.tab.table.insertRow(i)
            self.tab.table.setItem(i, 0, QtGui.QTableWidgetItem(str(gen)))
            self.tab.table.setItem(i, 1, QtGui.QTableWidgetItem(str(evals)))
            for j, (a, m, M) in enumerate(objectives):
                self.tab.table.setItem(
                    i, 2 + j, QtGui.QTableWidgetItem(str(a)))
            self.view.stats.chart.plot(objectives, evals, gen)
            QtCore.QTimer.singleShot(10, self.tab.table.scrollToBottom)

    # Slots
    def open_file(self):
        path, f = QtGui.QFileDialog.getOpenFileName(
            self.view, 'Open GAUDI Input',
            os.getcwd(), 'GAUDI Input (*.gaudi-input)')
        self.post_open_file(path)

    def open_file_from_dropdown(self, index):
        if index >= 0:
            path = self.tab.input_fld.itemText(index)
            self.post_open_file(path)

    def post_open_file(self, path):
        if path:
            self.parent().open_file(path)
            self.set_current()

    def process_started(self):
        # After GAUDI started
        print("Process started...")
        path = self.tab.input_fld.currentText()
        with open(path) as f:
            self.inputfile = yaml.load(f)
        self.tab.progressbar.reset()
        self.tab.progressbar.show()
        self.tab.progressbar.setMaximum(self.inputfile['ga']['gens'])
        self.tab.progressbar.setValue(0)

        self.tab.table.clear()
        self.tab.table.setRowCount(0)
        self.tab.table.setColumnCount(0)
        self.tab.table.setColumnCount(2 + len(self.inputfile['objectives']))
        headers = ['Generations', 'Evaluations'] + \
            ["{}{}".format('+-'[obj['weight'] < 0], obj['name'])
             for obj in self.inputfile['objectives']]
        self.tab.table.setHorizontalHeaderLabels(headers)

        self.tab.textbox.clear()
        self.parent().newjob.tab.bottom_run.setEnabled(False)
        self.tab.input_run.setEnabled(False)
        self.set_active()

        self.view.stats.chart.configure_plot(
            self.inputfile['ga']['gens'],
            self.inputfile['objectives'],
            self.inputfile['ga']['pop'])

        self.view.status('Running new job')
        self.tab.textbox.append('Running new job')

    def process_finished(self, exit_code, *args, **kwargs):
        self.parent().newjob.tab.bottom_run.setEnabled(True)
        self.tab.input_run.setEnabled(True)
        self.restore_enabled()

        self.view.status('Job Finished!')
        self.tab.textbox.append('Job Finished!')
        self.tab.progressbar.hide()

        # Load results
        if not exit_code:
            basedir = os.path.dirname(self.tab.input_fld.currentText())
            outputdir = self.inputfile['general']['outputpath']
            name = self.inputfile['general']['name'] + '.gaudi-output'
            path = os.path.normpath(os.path.join(basedir, outputdir, name))
            self.parent().open_file(path)
