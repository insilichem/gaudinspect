#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import isfile
import time
from PySide.QtCore import QSettings, Qt, Signal
from PySide.QtGui import QSortFilterProxyModel, QStandardItemModel, QStandardItem


class GAUDInspectModelRecentFiles(QStandardItemModel):

    KEY = "_recent_files"
    myDataChanged = Signal()

    def __init__(self):
        super().__init__(0, 1)
        self.settings = QSettings()
        self.populate()

    # Init methods
    def populate(self):
        files_and_timestamps = self.read_recent_files()
        if files_and_timestamps:
            for f, t in files_and_timestamps:
                self.add_entry(f, t)

    # Slots
    def add_entry(self, path, timestamp=None, sync=False, check_uniqueness=False):
        if timestamp is None:
            timestamp = int(time.time())
        item = QStandardItem(path)
        item.setData(timestamp, Qt.UserRole)
        self.insertRow(0, item)
        if check_uniqueness:
            self.delete_duplicates(path)
        if sync:
            self.model_to_recent()
            self.myDataChanged.emit()

    def clear_all(self):
        self.clear()
        self.clear_recent_files()
        self.myDataChanged.emit()

    def clear_deleted(self):
        files = [i for i in self.all_items() if isfile(i[0])]
        if files:
            self.write_recent_files(files)
            self.recent_to_model()
            self.myDataChanged.emit()
        else:
            self.clear_all()

    # Helpers
    def all_items(self):
        items = []
        for i in range(self.rowCount()):
            item = self.item(i)
            items.append((item.text(), item.data(Qt.UserRole)))
        return items

    def delete_duplicates(self, path):
        items = self.findItems(path)
        items.sort(key=lambda i: int(i.data(Qt.UserRole)), reverse=True)
        for item in items[1:]:
            self.removeRow(item.row())

    def recent_to_model(self):
        self.clear()
        self.populate()

    def model_to_recent(self):
        self.write_recent_files()

    # Data model
    def clear_recent_files(self):
        self.settings.remove(self.KEY)

    def read_recent_files(self):
        files_and_timestamps = []
        size = self.settings.beginReadArray(self.KEY)
        if size:
            for i in range(size):
                self.settings.setArrayIndex(i)
                data = self.settings.value(
                    "path"), self.settings.value("timestamp")
                files_and_timestamps.append(data)
            self.settings.endArray()
            files_and_timestamps.sort(key=lambda x: int(x[1]))
            return files_and_timestamps

    def write_recent_files(self, files_and_timestamps=None):
        if files_and_timestamps is None:
            files_and_timestamps = self.all_items()
        self.clear_recent_files()
        self.settings.beginWriteArray(self.KEY)
        for i, (path, timestamp) in enumerate(files_and_timestamps[:50]):
            self.settings.setArrayIndex(i)
            self.settings.setValue("path", path)
            self.settings.setValue("timestamp", timestamp)
        self.settings.endArray()

    @property
    def input_only(self):
        return GAUDInspectModelRecentFilesProxy(self, "*.gaudi-input")

    @property
    def output_only(self):
        return GAUDInspectModelRecentFilesProxy(self, "*.gaudi-output")


class GAUDInspectModelRecentFilesProxy(QSortFilterProxyModel):

    def __init__(self, model, wildcard, *args, **kwargs):
        super().__init__()
        self.setSourceModel(model)
        self.setFilterWildcard(wildcard)
