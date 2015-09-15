#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide.QtCore import Qt
from PySide import QtGui
from itertools import cycle


class GAUDInspectResultsController(object):

    def __init__(self, model, view, renderer='ballandstick', color='default'):
        # Models
        self.model = model
        self.proxy = CustomSortingModel(self.model)  # fix numerical sorting
        self.proxy.setSourceModel(self.model)
        # Tie them up
        self.view = view
        self.tableview = self.view.tabber.tabs[3].table
        self.tableview.setModel(self.proxy)
        self.tableview.sortByColumn(0, Qt.AscendingOrder)
        # Some parameters
        self.renderer = renderer
        self.colors = sorted(self.view.viewer.COLORS.keys())

        self.connect_signals()

    def connect_signals(self):
        selectionModel = self.tableview.selectionModel()
        selectionModel.selectionChanged.connect(self.selection_changed)

    def selection_changed(self, selected, deselected):
        self.view.viewer.clear()
        renderer = self.renderer
        mols = []
        # selection changed returns a list of selection ranges
        for s in selected:
            # each range has several items (cells)
            for i in s.indexes():
                # we only want cells in first column: the zip filename
                if i.column() == 0:
                    # Get item from original model, not proxy!
                    # Just use mapToSource instead of itemFromIndex
                    item = self.proxy.mapToSource(i)
                    mol2, meta = self.model.parse_zip(item.data())
                    for m, color in zip(mol2, cycle(self.colors)):
                        mols.append(m)
                        self.view.viewer.add_molecule(
                            m, renderer=renderer, color=color)
        if mols:
            self.view.viewer.focus(molecules=mols)


class CustomSortingModel(QtGui.QSortFilterProxyModel):

    """ A proxy model to fix numerical sorting """

    def lessThan(self, left, right):
        try:
            return float(left.data()) < float(right.data())
        except ValueError:
            return left.data() < right.data()
