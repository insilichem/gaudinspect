#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict

default = {

    "flags/configured": False,

    "paths/gaudi": "",
    "paths/chimera": "",

    "viewer/backgroundcolor": (0, 0, 0),
}

ADVANCED_OPTIONS_DEFAULT = OrderedDict([
    ('precision', [
        2,
        'Number of decimal numbers in output']),
    ('compress', [
        1,
        'Apply ZIP compression to results']),
    ('mu', [
        0.75,
        'Percentage of population to select for the next generation']),
    ('lambda_', [
        0.75,
        'Number of individuals (in terms of current population percentage) \nto create for at each generation']),
    ('mut_eta', [
        5,
        'Crowding degree of the mutation. A high eta will produce children \nresembling to their parents, while a small eta will produce solutions \nmuch more different']),
    ('mut_pb', [
        0.10,
        'The probability that an offspring is produced by mutation']),
    ('mut_indpb', [
        0.2,
        'The probability that a gene of a mutating individual is actually \nmutated']),
    ('cx_eta', [
        5,
        'Crowding degree of the crossover. A high eta will produce children \nresembling to their parents, while a small eta will produce solutions \nmuch more different']),
    ('cx_pb', [
        0.8,
        'The probability that an offspring is produced by crossover']),
    ('history', [
        False,
        'Record full history of evolution']),
    ('pareto', [
        False,
        'Use Pareto Front results (True) or Hall Of Fame results (False)']),
    ('similarity', [
        'gaudi.similarity.rmsd',
        'Function of similarity that will be used to discard similar \nindividuals']),
    ('similarity_args', [
        'Ligand, 0.5',
        'Positional arguments of similarity function']),
    ('similarity_kwargs', [
        '',
        'Optional arguments of similarity function'])
])
