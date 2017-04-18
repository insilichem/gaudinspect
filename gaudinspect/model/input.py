#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import


# Python
from copy import deepcopy
import yaml
from PyQt4.QtGui import QStandardItemModel


class GAUDInspectModelIn(QStandardItemModel):

    """
    Parses GAUDI input files
    """

    def __init__(self, path=None, *args, **kwargs):
        super(GAUDInspectModelIn, self).__init__()
        self.path = path
        if self.path:
            with open(path) as f:
                self._gaudidata = yaml.load(f)
                self.gaudidata = deepcopy(self._gaudidata)
        else:
            self.gaudidata = {'general': {},
                              'ga': {},
                              'similarity': {},
                              'genes': [],
                              'objectives': []
                              }

    def load(self, path, overwrite=True):
        with open(path) as f:
            self._gaudidata = yaml.load(f)
            if overwrite:
                self.gaudidata = deepcopy(self._gaudidata)
            else:
                self.gaudidata.update(deepcopy(self._gaudidata))

    def export(self, path):
        if not path.endswith('.gaudi-input'):
            path += '.gaudi-input'
        with open(path, 'w') as f:
            yaml.safe_dump(self.gaudidata, f, encoding='utf-8',
                           allow_unicode=True, default_flow_style=False)
