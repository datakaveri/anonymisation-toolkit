
.. .. automodule:: sanitisation
..    :members:

.. .. toctree::
..    :maxdepth: 3 ... autoapi/index
..    :caption: Contents:

.. Indices and tables
.. ==================
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`


===================
CDPG Anonymisation Toolkit
===================

Welcome to the documentation for the CDPG Anonymisation Toolkit!

.. image:: _static/CDPG_logo.png
   :alt: Project Logo
   :align: center

Overview
--------

In this toolkit, we provide a set of tools that a user can use to anonymise data. The provided functions can be used to preprocess and prepare the data for anonymisation, anonymise the data and then apply certain post-processing methods and obtain validation of the selected anonymisation method.

Quick Start
----------

.. code-block:: bash

   pip install cdpg-anonkit

.. code-block:: python

   import cdpg-anonkit
   
   # Quick example
   result = your_project.main_function()

Possible Operations
-----------

* Sanitisation
  * Clipping
  * Hashing
  * Suppression  
* Generalisation
  * Spatial Generalisation
  * Temporal Generalisation
  * Categorical Generalisation
* Aggregation
  * Query Building
* Differential Privacy
  * Sensitivity Computation
  * Noise Addition
* Post Processing 
  * Rounding and Clipping
  * Epsilon vs MAE

Contents
--------

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   installation
   quickstart
   api
   examples
   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`