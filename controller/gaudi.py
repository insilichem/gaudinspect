#!/usr/bin/python
# -*- coding: utf-8 -*-

from .base import GAUDInspectBaseController


class GaudiController(GAUDInspectBaseController):

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.fill_table()

    def fill_table(self):
        print self.model
