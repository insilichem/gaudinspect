#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide.QtCore import Qt
from chemlab.io import datafile
import subprocess
from chemlab.graphics import colors


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
        for i, path in enumerate(paths):
            if i % 2:
                color_scheme = colors.default_atom_map
            else:
                color_scheme = colors.light_atom_map
            pdb = path[:-4] + 'mol'
            cmd = [
                'C:/Program Files (x86)/OpenBabel-2.3.2/babel.exe', path, pdb]
            subprocess.call(cmd)
            mol = datafile(pdb).read('molecule')

            self.view.viewer.add_molecule(
                mol.r_array, mol.type_array, mol.bonds, color=color_scheme)
            self.view.viewer.camera.autozoom(mol.r_array)
            self.view.viewer.update()
