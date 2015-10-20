#!/usr/bin/python
# -*- coding: utf-8 -*-

from itertools import cycle
import operator

from PySide.QtCore import Qt
from PySide import QtGui

from .base import GAUDInspectBaseChildController


class GAUDInspectResultsController(GAUDInspectBaseChildController):

    def __init__(self, childmodel=None, renderer='ballandstick', color='default', **kwargs):
        super().__init__(**kwargs)
        self.tabindex = 3
        self.tab = self.view.tabber.tabs[self.tabindex]
        self.table = self.tab.table
        self.filters = self.tab.filter_group

        # Some parameters
        self.renderer = renderer
        self.colors = sorted(self.view.viewer.COLORS.keys())
        self.selected = []
        self.unzipped = {}

        if childmodel:
            self.set_model(childmodel)

    def set_model(self, model):
        # Models
        self.childmodel = model
        self.proxy = CustomSortFilterProxyModel(self.childmodel)
        self.proxy.setSourceModel(self.childmodel)
        self.table.setModel(self.proxy)
        self.table.sortByColumn(0, Qt.AscendingOrder)
        self.connect_model_signals()
        self.filters.show()
        self.tab.infotip.hide()
        self.set_active()

    def connect_model_signals(self):
        if not self.model:
            return
        selectionModel = self.table.selectionModel()
        selectionModel.selectionChanged.connect(self.selection_changed)

        self.filters.filter_add.clicked.connect(self.fill_filters)
        self.filters.filter_btn.clicked.connect(self.apply_filters)
        self.filters.filter_clear.clicked.connect(self.proxy.clear_filters)

    # Slots
    def clear(self):
        if not self.childmodel:
            return
        # Remove the model and filters
        self.childmodel.clear()
        self.model = None
        self.proxy.invalidate()
        self.filters.filter_clear.click()
        self.filters.hide()

        # Disconnect signals
        selectionModel = self.table.selectionModel()
        selectionModel.selectionChanged.disconnect(self.selection_changed)
        self.filters.filter_add.clicked.disconnect(self.fill_filters)
        self.filters.filter_btn.clicked.disconnect(self.apply_filters)
        self.filters.filter_clear.clicked.disconnect(
            self.proxy.clear_filters)

        # Clear the viewer
        self.view.viewer.clear()
        self.view.viewer.update()

        # Reenable all tabs
        self.tab.infotip.show()
        self.restore_enabled()

    def selection_changed(self, selected, deselected):
        self.view.viewer.clear()
        renderer = self.renderer
        mols = []
        # First, remove unselected items in this action
        to_deselect = []
        for d in deselected:
            # each range has several items (cells)
            for i in d.indexes():
                # we only want cells in first column: the zip filename
                if i.column() == 0:
                    # Get item from original model, not proxy!
                    # Just use mapToSource instead of itemFromIndex
                    item = self.proxy.mapToSource(i).data()
                    to_deselect.append(item)

        self.selected = [s for s in self.selected if s not in to_deselect]
        # Second, add new ones
        for s in selected:
            for i in s.indexes():
                if i.column() == 0:
                    item = self.proxy.mapToSource(i).data()
                    if item not in self.selected:
                        self.selected.append(item)

        # Now we have the full selection, add it to viewer
        for item in self.selected:
            try:
                mol2, meta = self.unzipped[item]
            except KeyError:
                mol2, meta = self.unzipped[
                    item] = self.childmodel.parse_zip(item)
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

    def _clear_cache(self):
        self.unzipped.clear()


class CustomSortFilterProxyModel(QtGui.QSortFilterProxyModel):

    """ A proxy model to fix numerical sorting """

    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.criteria[:] = criteria
        self.invalidateFilter()

    def clear_filters(self):
        del self.criteria[:]
        self.invalidateFilter()
