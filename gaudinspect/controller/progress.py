#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml
from PySide import QtCore, QtGui


class GAUDInspectProgressController(object):

    def __init__(self, parent, view, model=None):
        self.parent = parent
        self.model = model
        self.view = view
        self.tab = self.view.tabber.tabs[1]
        self.process = QtCore.QProcess(self.view)
        self.history = []
        self.inputfile = {}
        self.signals()

    def signals(self):
        self.parent.newjob.file_ready.connect(self.run)
        self.tab.input_btn.clicked.connect(self.open_file)
        self.tab.input_run.clicked.connect(self.run)
        self.process.readyReadStandardOutput.connect(self.report)
        self.process.started.connect(self.process_started)
        self.process.finished.connect(self.process_finished)

    def run(self, path=None):
        if path is None:
            path = self.tab.input_fld.text()
        else:
            self.tab.input_fld.setText(path)

        chimera = self.parent.app.settings.value("paths/chimera")
        gaudi = self.parent.app.settings.value(
            "paths/gaudi") + '/launch.py'
        args = ['--debug', '--nogui', '--silent', '--script',
                "{} {}".format(gaudi, path)]

        self.process.start(chimera, args)

    def open_file(self):
        path, f = QtGui.QFileDialog.getOpenFileName(
            self.view, 'Open GAUDI Input', os.getcwd(), 'GAUDI Input (*.in.gaudi)')
        if path:
            self.tab.input_fld.setText(path)

    def report(self):
        # Raw output
        line = str(self.process.readAllStandardOutput())
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
            return None, None, None
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
    def process_started(self):
        # After GAUDI started
        path = self.tab.input_fld.text()
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
        self.view.tabber.setCurrentIndex(1)
        self.parent.newjob.tab.bottom_run.setEnabled(False)
        self.tab.input_run.setEnabled(False)
        for i in [0, 2, 3]:
            self.view.tabber.setTabEnabled(i, False)

        self.view.stats.chart.configure_plot(
            self.inputfile['ga']['gens'],
            self.inputfile['objectives'],
            self.inputfile['ga']['pop'])

        self.view.status('Running new job')
        self.tab.textbox.append('Running new job')

    def process_finished(self, exitCode, *args, **kwargs):
        self.parent.newjob.tab.bottom_run.setEnabled(True)
        self.tab.input_run.setEnabled(True)
        for i in [0, 2, 3]:
            self.view.tabber.setTabEnabled(i, True)
        self.view.status('Job Finished!')
        self.tab.textbox.append('Job Finished!')
        self.tab.progressbar.hide()

        # Load results
        basedir = os.path.dirname(self.tab.input_fld.text())
        outputdir = self.inputfile['general']['outputpath']
        name = self.inputfile['general']['name'] + '.out.gaudi'
        path = os.path.normpath(os.path.join(basedir, outputdir, name))
        self.parent._open_file(path)
