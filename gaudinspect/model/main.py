#!/usr/bin/python
# -*- coding: utf-8 -*-

# GAUDInspect
from .output import GAUDInspectModelOut
from .input import GAUDInspectModelIn
from .recent import GAUDInspectModelRecentFiles


class GAUDInspectModel(object):

    """
    Wrapper function to choose correct model based on input file
    """

    def __init__(self, app=None):
        self.app = app
        self.recent = GAUDInspectModelRecentFiles()

    @classmethod
    def get(self, data):
        if data.endswith('.out.gaudi'):
            self.results = model = GAUDInspectModelOut(data)
        elif data.endswith('.in.gaudi'):
            self.newjob = model = GAUDInspectModelIn(data)
        else:
            print('ERROR! Format unknown.')
            return

        return model
