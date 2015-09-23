#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import random
import string
from collections import OrderedDict
from copy import deepcopy
from PySide import QtGui
from pprint import pprint


class GAUDInspectNewJobController(object):

    FIELDS = {
        'general_generations_field': ('ga', 'gens', int),
        'general_population_field': ('ga', 'pop', int),
        'general_project_field': ('general', 'name', str),
        'general_outputpath_field': ('general', 'outputpath', str)
    }

    ADVANCED_OPTIONS_DEFAULT = OrderedDict([
        ('precision', [
            2,
            'Number of decimal numbers in output']),
        ('compress', [
            1,
            'Apply ZIP compression to results']),
        ('mu', [
            0.75,
            'Percentage of population to select for the next generation']),
        ('lambda_', [
            0.75,
            'Number of individuals (in terms of current population percentage) \nto create for at each generation']),
        ('mut_eta', [
            5,
            'Crowding degree of the mutation. A high eta will produce children \nresembling to their parents, while a small eta will produce solutions \nmuch more different']),
        ('mut_pb', [
            0.10,
            'The probability that an offspring is produced by mutation']),
        ('mut_indpb', [
            0.2,
            'The probability that a gene of a mutating individual is actually \nmutated']),
        ('cx_eta', [
            5,
            'Crowding degree of the crossover. A high eta will produce children \nresembling to their parents, while a small eta will produce solutions \nmuch more different']),
        ('cx_pb', [
            0.8,
            'The probability that an offspring is produced by crossover']),
        ('history', [
            False,
            'Record full history of evolution']),
        ('pareto', [
            False,
            'Use Pareto Front results (True) or Hall Of Fame results (False)']),
        ('similarity', [
            'gaudi.similarity.rmsd',
            'Function of similarity that will be used to discard similar \nindividuals']),
        ('similarity_args', [
            'Ligand, 0.5',
            'Positional arguments of similarity function']),
        ('similarity_kwargs', [
            '',
            'Optional arguments of similarity function'])
    ])

    def __init__(self, parent, view, model=None):
        self.parent = parent
        self.model = model
        self.view = view
        self.form = self.view.tabber.tabs[0]
        self._connect_signals()
        self.advanced_options = deepcopy(self.ADVANCED_OPTIONS_DEFAULT)
        if model:
            self.set_model(model)
        self.form.advanced_dialog.fill_table(self.advanced_options)

    def set_model(self, model):
        self.model = model
        self.load_data()
        self.view.tabber.setCurrentIndex(0)

    def export(self):

        path, format = QtGui.QFileDialog.getSaveFileName(
            self.view, 'Save this GAUDI input', os.getcwd(), "GAUDI Input (*.in.gaudi)")
        if path:
            self.dump_data_to_model()
            self.model.export(path)

    # Signals
    def _connect_signals(self):
        self.form.general_project_btn.clicked.connect(self._random_name)
        self.form.general_outputpath_browse.clicked.connect(self._choose_path)
        self.form.advanced_btn.clicked.connect(self.form.advanced_dialog.exec)
        self.form.advanced_dialog.default_btn.clicked.connect(
            lambda: self.form.advanced_dialog.fill_table(self.ADVANCED_OPTIONS_DEFAULT))
        self.form.bottom_save.clicked.connect(self.export)

    # Slots
    def load_data(self):
        if self.model:
            for k, (v, w, t) in self.FIELDS.items():
                getattr(self.form, k).setText(str(self.model.gaudidata[v][w]))

            for gene in self.model.gaudidata['genes']:
                item = QtGui.QListWidgetItem(
                    '{} ({})'.format(gene['name'], gene['type']))
                item.params = gene
                self.form.genes_list.addItem(item)

            for obj in self.model.gaudidata['objectives']:
                item = QtGui.QListWidgetItem(
                    '{} ({})'.format(obj['name'], obj['type']))
                item.params = obj
                self.form.objectives_list.addItem(item)

            # Replace default advanced settings
            for k, v in self.model.gaudidata['general'].items():
                self.advanced_options.get(k, ['_'])[0] = v
            for k, v in self.model.gaudidata['ga'].items():
                self.advanced_options.get(k, ['_'])[0] = v
            self.advanced_options['similarity'][0] = \
                self.model.gaudidata['similarity']['type']
            self.advanced_options['similarity_args'][0] = \
                self.model.gaudidata['similarity']['args']
            self.advanced_options['similarity_kwargs'][0] = \
                self.model.gaudidata['similarity']['kwargs']

        self.form.advanced_dialog.fill_table(self.advanced_options)

    def dump_data_to_model(self):
        if self.model:
            for k, (v, w, t) in self.FIELDS.items():
                self.model.gaudidata[v][w] = t(getattr(self.form, k).text())

            del self.model.gaudidata['genes'][:]
            for i in range(self.form.genes_list.count()):
                item = self.form.genes_list.item(i)
                self.model.gaudidata['genes'].append(item.params)

            del self.model.gaudidata['objectives'][:]
            for i in range(self.form.objectives_list.count()):
                item = self.form.objectives_list.item(i)
                self.model.gaudidata['objectives'].append(item.params)

            # Replace default advanced settings
            for k, v in self.model.gaudidata['general'].items():
                v = self.advanced_options.get(k, ['_'])[0]
            for k, v in self.model.gaudidata['ga'].items():
                v = self.advanced_options.get(k, ['_'])[0]
            self.model.gaudidata['similarity']['type'] = \
                self.advanced_options['similarity'][0]
            self.model.gaudidata['similarity']['args'] =  \
                self.advanced_options['similarity_args'][0]
            self.model.gaudidata['similarity']['kwargs'] = \
                self.advanced_options['similarity_kwargs'][0]

    def _random_name(self):
        s = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(8))
        self.form.general_project_field.setText(s)

    def _choose_path(self):
        path = QtGui.QFileDialog.getExistingDirectory(
            self.form, 'Choose a directory', os.getcwd())
        self.form.general_outputpath_field.setText(path)
