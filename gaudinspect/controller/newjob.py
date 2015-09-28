#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import random
import string
import yaml
import importlib
from collections import OrderedDict
from copy import deepcopy
from PySide import QtGui, QtCore

from ..view.dialogs.extension import GAUDInspectConfigureExtension


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
        # Genes
        self.form.genes_add.clicked.connect(self._gene_add)
        self.form.genes_del.clicked.connect(self._gene_del)
        self.form.genes_cfg.clicked.connect(self._gene_cfg)
        # Objectives
        self.form.objectives_add.clicked.connect(self._objective_add)
        self.form.objectives_del.clicked.connect(self._objective_del)
        self.form.objectives_cfg.clicked.connect(self._objective_cfg)
        # General
        self.form.general_project_btn.clicked.connect(self._random_name)
        self.form.general_outputpath_browse.clicked.connect(self._choose_path)
        self.form.advanced_btn.clicked.connect(self.form.advanced_dialog.exec_)
        self.form.bottom_save.clicked.connect(self.export)

    # Slots
    def load_data(self):
        if self.model:
            for k, (v, w, t) in self.FIELDS.items():
                getattr(self.form, k).setText(str(self.model.gaudidata[v][w]))

            for gene in self.model.gaudidata['genes']:
                item = self._create_data_listitem(gene)
                self.form.genes_list.addItem(item)

            for obj in self.model.gaudidata['objectives']:
                item = self._create_data_listitem(obj)
                self.form.objectives_list.addItem(item)

            # Replace default advanced settings
            for k, v in self.model.gaudidata['general'].items():
                self.advanced_options.get(k, ['_'])[0] = v
            for k, v in self.model.gaudidata['ga'].items():
                self.advanced_options.get(k, ['_'])[0] = v
            self.advanced_options['similarity'][0] = \
                self.model.gaudidata['similarity']['module']
            self.advanced_options['similarity_args'][0] = \
                self.model.gaudidata['similarity']['args']
            self.advanced_options['similarity_kwargs'][0] = \
                self.model.gaudidata['similarity']['kwargs']

        self.form.advanced_dialog.fill_table(self.advanced_options)

    def dump(self):
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
            self.model.gaudidata['similarity'][
                'type'] = self.advanced_options['similarity'][0]
            self.model.gaudidata['similarity'][
                'args'] = self.advanced_options['similarity_args'][0]
            self.model.gaudidata['similarity'][
                'kwargs'] = self.advanced_options['similarity_kwargs'][0]

    def _create_item(self, d=None, meta={}):
        gaudipath = self.parent.app.settings.value("general/gaudipath")

        if 'module' in meta:
            gaudi, type_, module = meta['module'].split('.')
            extension = os.path.join(
                gaudipath, type_, module) + '.gaudi-extension'
        elif d:
            extension, f = QtGui.QFileDialog.getOpenFileName(
                self.view, 'Load GAUDI extension', os.path.join(gaudipath, d),
                "GAUDI Extension (*.gaudi-extension);; All files (*.*)")
            if not extension:
                return
        else:
            print("Please provide type of extension or already populated dict")
            return

        with open(extension) as f:
            definitions = yaml.load(f)

        params, ok = GAUDInspectConfigureExtension.process(
            self.view, definitions, values=meta)
        if ok:
            return self._create_data_listitem(params)

    def _update_item(self, item):
        new = self._create_item(meta=item.data(QtCore.Qt.UserRole))
        if new:
            item.setText(new.text())
            item.setData(QtCore.Qt.UserRole, new.data(QtCore.Qt.UserRole))

    # Actions
    # Gene & Objective actions
    def _gene_add(self):
        item = self._create_item(d='genes')
        self.form.genes_list.addItem(item)

    def _gene_del(self):
        i = self.form.genes_list.currentRow()
        if i is not None:
            item = self.form.genes_list.takeItem(i)
            del item

    def _gene_cfg(self):
        item = self.form.genes_list.currentItem()
        if item is not None:
            self._update_item(item)

    def _objective_add(self):
        item = self._create_item(d='objectives')
        self.form.objectives_list.addItem(item)

    def _objective_del(self):
        i = self.form.objectives_list.currentRow()
        if i is not None:
            item = self.form.objectives_list.takeItem(i)
            del item

    def _objective_cfg(self):
        item = self.form.objectives_list.currentItem()
        if item is not None:
            self._update_item(item)

    # General actions
    def _random_name(self):
        s = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(8))
        self.form.general_project_field.setText(s)

    def _choose_path(self):
        path = QtGui.QFileDialog.getExistingDirectory(
            self.form, 'Choose a directory', os.getcwd())
        self.form.general_outputpath_field.setText(path)

    # Helper
    @staticmethod
    def _create_data_listitem(params):
        item = QtGui.QListWidgetItem(
            '{} ({})'.format(params['name'], params['module']))
        item.setData(QtCore.Qt.UserRole, params)
        return item
