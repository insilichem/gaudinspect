#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide.QtCore import Qt
from chemlab.io import datafile
import subprocess
from chemlab.graphics import colors
import os
import numpy as np

if os.name == 'nt':
    BABEL = 'C:/Program Files (x86)/OpenBabel-2.3.2/babel.exe'
elif os.name == 'posix':
    BABEL = 'babel'
else:
    BABEL = input('Please specify path to babel binary:\n')


class GAUDInspectController(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.fill_table()
        self.connect_signals()

    def fill_table(self):
        self.tableview = self.view.tabber.tabs[3].table
        self.tableview.setModel(self.model)
        self.tableview.sortByColumn(0, Qt.AscendingOrder)

    def connect_signals(self):
        selectionModel = self.tableview.selectionModel()
        selectionModel.selectionChanged.connect(self.selection_changed)

    def selection_changed(self, selected, deselected):
        self.view.viewer.clear_view()
        for s in selected:
            i = s.indexes()[0]
            item = self.model.itemFromIndex(i)
            mol2, meta = self.model.parse_zip(item.text())
            self.add_to_viewer(*mol2)

    def add_to_viewer(self, *paths):
        all_coords = []
        for i, path in enumerate(paths):
            if i % 2:
                color_scheme = colors.default_atom_map
            else:
                color_scheme = colors.light_atom_map
            mol = datafile(path).read('molecule')

            self.view.viewer.add_molecule(
                mol.r_array, mol.type_array, mol.bonds, color=color_scheme)
            all_coords.append(mol.r_array)
            self.view.viewer.update()

        self.view.viewer.camera.autozoom(np.concatenate(all_coords))
