.. FYS4565 code library documentation master file, created by
   sphinx-quickstart on Mon Jan  8 14:20:44 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
=============
This page contains the documentation for the code library that we will use for FYS4565.
It is organized into Python modules, as described below.

To install the library, copy the python files or `git clone` from https://github.com/AcceleratorPhysicsUiO/FYS4565-codelibrary
The repository also contains Jupyter notebooks with examples on how to use the modules.

Python modules
===============

The Python modules are described below.
To use them, place them in the folder of your notebook or python script and import it.

ParticleBeamManager
-------------------

.. automodule:: ParticleBeamManager
    :members:

BeamlineElements
--------------------

.. automodule:: BeamlineElements
    :members:

BeamLine
--------

.. automodule:: BeamLine
.. autoclass:: ElementSequence
    :members:
    :special-members:
    :inherited-members:

ParticleBeamPlotter
--------------------

.. automodule:: ParticleBeamPlotter
    :members:

Util
----

.. automodule:: Util
    :members:


.. toctree::
   :maxdepth: 2
   :caption: Contents:


..
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
