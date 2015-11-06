GAUDInspect
===========

A GUI for GAUDI input creation and output inspection.

*It will also allow to visually inspect the optimization process step-by-step to know how the system will behave during the essay.*

Installation
------------

The easiest way to install ``GAUDInspect`` in your computer is using the Anaconda Python distribution, which provides already built packages and a useful environments and packages CLI manager called ``conda``. However, you don't need the whole Anaconda package; it's enough with ``conda``, which is distributed as ``miniconda``.

1 - First, install `Miniconda for Python 3 <http://conda.pydata.org/miniconda.html>`_. Instructions can be found `here <http://conda.pydata.org/docs/install/quick.html#miniconda-quick-install-requirements>`_.

2 - By default, conda will only look for packages in the default repository. We use some custom builds that are distributed in separate (and, some of them, private) channels that must be added to the configuration. Open up a text editor and paste the following lines. 

.. code-block:: yaml

    channels:
      - http://klingon.uab.cat/repo/jaime/conda
      - omnia
      - pyzo
      - gabrielelanaro
      - defaults
 

3 - Then, save the file as ``.condarc`` in your home directory. That will be ``/home/<your_user>/.condarc`` for Linux, and ``C:/Users/<your_user>/.condarc`` for Windows.

4 - Create a new environment to deploy GAUDInspect. Since you have already the channels, it's as easy as typing ``conda create -n <name> gaudinspect``. Choose any name (like, why not, ``gaudinspect``). For example, ``conda create -n gaudinspect gaudinspect``. Conda will take care of resolving the dependencies, which can involve some downloading. 

5 - When it's done, Conda will instruct you how to activate your new environment with something like this:

.. code-block:: yaml

    # Windows
    # To activate this environment, use:
    # > activate gaudinspect
    #
    # Linux
    # To activate this environment, use:
    # > source activate gaudinspect
    #


6 - Activate the environment and run ``gaudinspect``, which should bring up the GUI promting about the configuration.

Configuration
-------------

GAUDInspect needs some small configuration to run GAUDI jobs. Mainly, the path to ``GAUDI`` and the path to ``UCSF Chimera`` binary. If you have not installed GAUDI yet, please refer its `installation guide <https://bitbucket.org/jrgp/gaudi>`_.