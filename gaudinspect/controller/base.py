#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc


class GaudiViewBaseController(metaclass=abc.ABCMeta):

    """
    Document this!
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass
