#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import


# Python
import os
import tempfile
import yaml
import zipfile
from PyQt4.QtGui import QStandardItemModel, QStandardItem


class GAUDInspectModelOut(QStandardItemModel):

    """
    Parses GAUDI output files and processes resulting Zip files.

    .. todo::

        Process metadata files (rotamers, h bonds, clashes).

        Cache the protein file if possible.

    """

    def __init__(self, path, *args, **kwargs):
        super(GAUDInspectModelOut, self).__init__()
        self.path = path
        self.basedir = os.path.dirname(path)
        self.tempdir = tempfile.mkdtemp('gaudinspect')
        self.parse()

    def parse(self):
        """
        Since the output files are already YAML-formatted, we
        only need to load them with PyYaml.
        """
        with open(self.path) as f:
            self._data = yaml.load(f)

        self.genes = {}
        self.objectives = self._data['GAUDI.objectives']
        self.results = self._data['GAUDI.results']

        self.setColumnCount(len(self.objectives) + 1)
        self.setHorizontalHeaderLabels(['Individual'] + self.objectives)
        row = 0
        for ind, val in self.results.items():
            col = 0
            self.insertRow(row)
            self.setItem(row, col, QStandardItem(ind))
            for v in val:
                col += 1
                self.setItem(row, col, QStandardItem(str(v)))

            row += 1

    def parse_zip(self, entrypath):
        """
        GAUDI zips its results files. We extract them on the fly to temp
        directories and feed the abs paths to the corresponding controllers.
        """
        path = os.path.join(self.basedir, entrypath)
        try:
            z = zipfile.ZipFile(path)
        except zipfile.BadZipfile:
            print("Not a valid GAUDI result")
        else:
            tmp = os.path.join(
                self.tempdir, os.path.splitext(os.path.basename(path))[0])
            try:
                os.mkdir(tmp)
            except OSError:  # Assume it exists
                pass
            z.extractall(tmp)
            mol2 = []
            meta = z.namelist()
            for name in sorted(os.listdir(tmp)):
                absname = os.path.join(tmp, name)
                if name.endswith(".mol2"):
                    mol2.append(os.path.normpath(absname))
                elif name.endswith(".yaml"):
                    meta.append(os.path.normpath(absname))
            return mol2, meta
        finally:
            z.close()

    def clear(self):
        super(GAUDInspectModelOut, self).clear()
        self._data.clear()
        self.objectives.clear()
        self.genes.clear()
        self.results.clear()
