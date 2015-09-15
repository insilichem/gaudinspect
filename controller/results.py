#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide.QtCore import Qt
from PySide import QtGui
from itertools import cycle
import operator


class GAUDInspectResultsController(object):

    def __init__(self, model, view, renderer='ballandstick', color='default'):
        # Models
        self.model = model
        self.proxy = CustomSortFilterProxyModel(self.model)
        self.proxy.setSourceModel(self.model)
        # Tie them up
        self.view = view
        self.tableview = self.view.tabber.tabs[3].table
        self.tableview.setModel(self.proxy)
        self.tableview.sortByColumn(0, Qt.AscendingOrder)
        self.filters = self.view.tabber.tabs[3].filter_group
        # Some parameters
        self.renderer = renderer
        self.colors = sorted(self.view.viewer.COLORS.keys())

        self.connect_signals()

    def connect_signals(self):
        selectionModel = self.tableview.selectionModel()
        selectionModel.selectionChanged.connect(self.selection_changed)

        self.filters.filter_add.clicked.connect(self.fill_filters)
        self.filters.filter_btn.clicked.connect(self.apply_filters)
        self.filters.filter_clear.clicked.connect(self.proxy.clear_filters)

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

    def apply_filters(self):
        self.proxy.clear_filters()
        criteria = []
        for f in self.filters.filters:
            column = f.key.currentIndex() + 1
            operator = f.operator.currentText()
            value = f.value.text()
            criteria.append([column, operator, value])
        self.proxy.setFilterFixedString(criteria)

    def fill_filters(self):
        f = self.filters.filters[-1]
        f.type.currentIndexChanged.connect(lambda: self.fill_filter_keys(f))

    def fill_filter_keys(self, f):
        f.key.clear()
        try:
            f.key.addItems(getattr(self.model,
                                   f.type.currentText().lower()))
        except AttributeError:
            pass


class CustomSortFilterProxyModel(QtGui.QSortFilterProxyModel):

    """ A proxy model to fix numerical sorting """

    def __init__(self, parent=None):
        super(CustomSortFilterProxyModel, self).__init__(parent)
        self.functions = {
            '>': operator.gt,
            '>=': operator.ge,
            '<': operator.lt,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne,
            'contains': operator.contains}
        self.criteria = []

    def lessThan(self, left, right):
        try:
            return float(left.data()) < float(right.data())
        except ValueError:
            return left.data() < right.data()

    def filterAcceptsRow(self, row, parent):
        model = self.sourceModel()
        tests = [self.functions[op](float(model.item(row, col).text()), float(val))
                 for col, op, val in self.criteria]
        return not False in tests

    def setFilterFixedString(self, criteria):
        self.criteria = criteria
        self.invalidateFilter()

    def clear_filters(self):
        del self.criteria[:]
        self.invalidateFilter()
