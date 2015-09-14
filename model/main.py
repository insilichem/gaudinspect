#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python
from collections import OrderedDict
import zipfile
import tempfile
import os
# External dependencies
import yaml
from PySide.QtGui import QStandardItemModel, QStandardItem


def GAUDInspectModel(path):
    """
    Wrapper function to choose correct model based on input file
    """
    if path.endswith('.out.gaudi'):
        model = GAUDInspectModelOut(path)
    elif path.endswith('.in.gaudi'):
        model = GAUDInspectModelIn(path)
    else:
        print('ERROR! Format unknown.')
        return

    return model


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
        self.tempdir = tempfile.mkdtemp('gaudiview')
        self.parse()

    def parse(self):
        """
        Since the output files are already YAML-formatted, we
        only need to load them with PyYaml.
        """
        with open(self.path) as f:
            self.gaudidata = yaml.load(f)

        self.setColumnCount(len(self.gaudidata['GAUDI.objectives']) + 1)
        self.setHorizontalHeaderLabels(
            ['Individual'] + self.gaudidata['GAUDI.objectives'])
        row = 0
        for ind, val in self.gaudidata['GAUDI.results'].items():
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
