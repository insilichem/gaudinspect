#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import
import os
import random
import string
import yaml
from copy import deepcopy
from functools import partial

from PyQt4 import QtGui, QtCore

from .base import GAUDInspectBaseChildController
from ..model.input import GAUDInspectModelIn
from ..view.dialogs.extension import GAUDInspectConfigureExtension
from ..view.dialogs.advanced import GAUDInspectAdvancedOptionsDialog
from ..configuration import ADVANCED_OPTIONS_DEFAULT


class GAUDInspectNewJobController(GAUDInspectBaseChildController):

    FIELDS = {
        'general_generations_field': ('ga', 'gens'),
        'general_population_field': ('ga', 'pop'),
        'general_project_field': ('general', 'name'),
        'general_outputpath_field': ('general', 'outputpath')
    }

    file_ready = QtCore.pyqtSignal(str)

    def __init__(self, childmodel=None, **kwargs):
        super(GAUDInspectNewJobController, self).__init__(**kwargs)
        self.tabindex = 0
        self.tab = self.view.tabber.tabs[self.tabindex]
        self.advanced_options = deepcopy(ADVANCED_OPTIONS_DEFAULT)
        self.MODIFIED = False
        self.SAVE_PATH = None

        self.signals()
        if childmodel:
            self.set_model(childmodel)
        else:
            self.childmodel = GAUDInspectModelIn()

    def set_model(self, model):
        self.childmodel = model
        self.load_data()
        self.set_current()

    def export(self):
        path, format = QtGui.QFileDialog.getSaveFileName(
            self.view, 'Save this GAUDI input',
            os.getcwd(), "GAUDI Input (*.gaudi-input)")
        if path:
            self.dump()
            self.childmodel.export(path)
            self.SAVE_PATH = path
            self.view.status("File saved at {}.".format(path))
            return path

    # Signals
    def signals(self):
        # Genes
        self.tab.genes_add.clicked.connect(self._gene_add)
        self.tab.genes_del.clicked.connect(self._gene_del)
        self.tab.genes_cfg.clicked.connect(self._gene_cfg)
        # Objectives
        self.tab.objectives_add.clicked.connect(self._objective_add)
        self.tab.objectives_del.clicked.connect(self._objective_del)
        self.tab.objectives_cfg.clicked.connect(self._objective_cfg)
        # General
        self.tab.general_project_btn.clicked.connect(self._random_name)
        self.tab.general_outputpath_browse.clicked.connect(self._choose_path)
        self.tab.advanced_btn.clicked.connect(partial(
            GAUDInspectAdvancedOptionsDialog.process,
            self.view, self.advanced_options))
        # Bottom buttons
        self.tab.bottom_save.clicked.connect(self.export)
        self.tab.bottom_run.clicked.connect(self._save_and_run)

    # Slots
    def load_data(self):
        if self.childmodel:
            for k, (v, w) in self.FIELDS.items():
                getattr(self.tab, k).setText(
                    str(self.childmodel.gaudidata[v][w]))

            for gene in self.childmodel.gaudidata['genes']:
                item = self._create_data_listitem(gene)
                self.tab.genes_list.addItem(item)

            for obj in self.childmodel.gaudidata['objectives']:
                item = self._create_data_listitem(obj)
                self.tab.objectives_list.addItem(item)

            # Replace default advanced settings
            for k, v in self.childmodel.gaudidata['general'].items():
                self.advanced_options.get(k, [''])[0] = v
            for k, v in self.childmodel.gaudidata['ga'].items():
                self.advanced_options.get(k, [''])[0] = v
            self.advanced_options['similarity'][0] = \
                self.childmodel.gaudidata['similarity']['module']
            self.advanced_options['similarity_args'][0] = \
                self.childmodel.gaudidata['similarity']['args']
            self.advanced_options['similarity_kwargs'][0] = \
                self.childmodel.gaudidata['similarity']['kwargs']

            self.SAVE_PATH = self.childmodel.path

    def dump(self):
        if self.childmodel:
            for k, (v, w) in self.FIELDS.items():
                self.childmodel.gaudidata[v][w] = yaml.load(
                    getattr(self.tab, k).text())

            del self.childmodel.gaudidata['genes'][:]
            for i in range(self.tab.genes_list.count()):
                item = self.tab.genes_list.item(i)
                self.childmodel.gaudidata['genes'].append(
                    item.data(QtCore.Qt.UserRole))

            del self.childmodel.gaudidata['objectives'][:]
            for i in range(self.tab.objectives_list.count()):
                item = self.tab.objectives_list.item(i)
                self.childmodel.gaudidata['objectives'].append(
                    item.data(QtCore.Qt.UserRole))

            # Replace default advanced settings
            for k in self.childmodel.gaudidata['general']:
                value = self.advanced_options.get(k, [''])[0]
                if value:
                    self.childmodel.gaudidata['general'][k] = \
                        yaml.load(str(value))
            for k in self.childmodel.gaudidata['ga']:
                value = self.advanced_options.get(k, [''])[0]
                if value:
                    self.childmodel.gaudidata['ga'][k] = yaml.load(str(value))
            self.childmodel.gaudidata['similarity']['module'] = \
                self.advanced_options['similarity'][0]
            self.childmodel.gaudidata['similarity']['args'] = \
                self.advanced_options['similarity_args'][0]
            self.childmodel.gaudidata['similarity']['kwargs'] = \
                self.advanced_options['similarity_kwargs'][0]

            self.MODIFIED = False

    def _create_item(self, d=None, meta={}):
        gaudipath = self.parent().app.settings.value(
            "paths/gaudi") + '/gaudi'

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
            self.MODIFIED = True
            return self._create_data_listitem(params)

    def _update_item(self, item):
        new = self._create_item(meta=item.data(QtCore.Qt.UserRole))
        if new:
            self.MODIFIED = True
            item.setText(new.text())
            item.setData(QtCore.Qt.UserRole, new.data(QtCore.Qt.UserRole))

    # Actions
    # Gene & Objective actions
    def _gene_add(self):
        item = self._create_item(d='genes')
        self.tab.genes_list.addItem(item)

    def _gene_del(self):
        i = self.tab.genes_list.currentRow()
        if i is not None:
            item = self.tab.genes_list.takeItem(i)
            del item

    def _gene_cfg(self):
        item = self.tab.genes_list.currentItem()
        if item is not None:
            self._update_item(item)

    def _objective_add(self):
        item = self._create_item(d='objectives')
        self.tab.objectives_list.addItem(item)

    def _objective_del(self):
        i = self.tab.objectives_list.currentRow()
        if i is not None:
            item = self.tab.objectives_list.takeItem(i)
            del item

    def _objective_cfg(self):
        item = self.tab.objectives_list.currentItem()
        if item is not None:
            self._update_item(item)

    # General actions
    def _random_name(self):
        s = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(8))
        self.tab.general_project_field.setText(s)

    def _choose_path(self):
        path = QtGui.QFileDialog.getExistingDirectory(
            self.tab, 'Choose a directory', os.getcwd())
        if path:
            self.tab.general_outputpath_field.setText(path)

    def _save_and_run(self):
        if self.MODIFIED:
            self.export()
        self.file_ready.emit(self.SAVE_PATH)

    # Helper
    @staticmethod
    def _create_data_listitem(params):
        item = QtGui.QListWidgetItem(
            '{} ({})'.format(params['name'], params['module']))
        item.setData(QtCore.Qt.UserRole, params)
        return item
