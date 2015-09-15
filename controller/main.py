#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc
from . import results


class GAUDInspectController(metaclass=abc.ABCMeta):

    """
    Document this!
    """

    def __init__(self, *args, **kwargs):
        self.results = results.GAUDInspectResultsController(*args)
