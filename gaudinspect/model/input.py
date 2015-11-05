#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python
from copy import deepcopy
import yaml
from PySide.QtGui import QStandardItemModel


class GAUDInspectModelIn(QStandardItemModel):

    """
    Parses GAUDI input files
    """

    def __init__(self, path, *args, **kwargs):
        super(GAUDInspectModelIn, self).__init__()
        self.path = path
        with open(path) as f:
            self._gaudidata = yaml.load(f)
            self.gaudidata = deepcopy(self._gaudidata)

    def export(self, path):
        if not path.endswith('.gaudi-input'):
            path = path + '.gaudi-input'
        with open(path, 'w') as f:
            yaml.dump(self.gaudidata, f, default_flow_style=False)
