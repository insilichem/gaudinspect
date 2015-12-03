from __future__ import print_function
from setuptools import setup, find_packages
import io
import os

import gaudinspect

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')

setup(
    name='gaudinspect',
    version=gaudinspect.__version__,
    url='https://bitbucket.org/jrgp/gaudinspect',
    license='Free For Educational Use',
    author='Jaime Rodriguez-Guerra Pedregal',
    author_email='jaime.rogue@gmail.com',
    description='A full GUI for launching GAUDI jobs, '
                'analyze their progress, and examine the results.',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Science/Research',
        'License :: Free For Educational Use',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Chemistry',
    ],
    scripts=['scripts/gaudinspect']
)
