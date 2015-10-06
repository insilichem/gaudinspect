#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy


def get(parent=None):
    return GAUDInspectViewStats(parent=parent)


class GAUDInspectViewStats(QtGui.QWidget):

    def __init__(self, parent=None):
        super(GAUDInspectViewStats, self).__init__()
        self.setParent(parent)
        self.parent = parent
        self.hide()
        self.initUI()

    def initUI(self):
        self.layout = QtGui.QVBoxLayout(self)
        self.chart = GAUDInspectChartCanvas(self)
        self.layout.addWidget(self.chart)
        # Disable margins
        for obj in (self, self.layout, self.chart):
            try:
                obj.setContentsMargins(0, 0, 0, 0)
                obj.setSpacing(0)
            except AttributeError:
                pass


class GAUDInspectChartCanvas(QtGui.QWidget):

    def __init__(self, parent=None):
        super(GAUDInspectChartCanvas, self).__init__(parent)
        self.initUI()

    def initUI(self):
        plt.style.use('fivethirtyeight')
        plt.rc('font', size=12)

        self.figure = plt.figure()
        self.figure.patch.set_alpha(0)
        self.ax1 = self.figure.add_subplot(
            111, axis_bgcolor='none',
            xlim=(0, 20), ylim=(0, 1000),
            xlabel='Generations')
        self.ax2 = self.ax1.twinx()
        self.canvas = FigureCanvas(self.figure)
        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.figure.tight_layout()

    def configure_plot(self, generations, objectives, population):
        self.ax1.clear()
        self.ax1.set_axis_bgcolor('none')
        self.ax1.set_xlabel('Generations')
        self.ax1.set_ylabel('Average score')
        self.ax1.set_autoscalex_on(False)
        self.ax1.set_xlim(1, generations)
        self.ax1.set_autoscaley_on(True)

        # Create a line plotter for each objective
        self.lines = []
        for obj in objectives:
            line, = self.ax1.plot([], label=obj['name'])
            self.lines.append(line)

        # Create legend for objectives
        self.legend = plt.legend(*self.ax1.get_legend_handles_labels(),
                                 loc='upper left', fancybox=True, framealpha=0.8)

        # Get a second Y axis for evaluations
        self.ax2.set_ylim(0, population)
        self.ax2.set_xlim(1, generations)
        self.ax2.set_ylabel('Individuals evaluated')
        self.ax2.grid(b=False)
        # Fix Z-ordering of axes
        self.ax1.set_zorder(self.ax2.get_zorder() + 1)

        # Draw evaluations per generation
        self.rects = self.ax2.bar(
            range(1, generations + 1), [0] * generations,
            align='center', color='0.85')

        # Move legend to top
        self.ax1.add_artist(self.legend)
        self.ax2.legend = None

        self.figure.tight_layout()
        self.canvas.draw()

    def plot(self, objectives, evals, gen):
        self.rects[gen - 1].set_height(evals)
        for line, obj in zip(self.lines, objectives):
            line.set_data(numpy.append(line.get_xdata(), gen),
                          numpy.append(line.get_ydata(), obj[0]))
        # Update view (yes, all these commands are compulsory)
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.figure.tight_layout()
        self.canvas.draw()
