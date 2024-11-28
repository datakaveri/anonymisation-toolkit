
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

.. image:: _static/logo.png
   :alt: Project Logo
   :align: center

Overview
--------

In this toolkit, we provide a set of tools that a user can use to anonymise data. The provided functions can be used to preprocess and prepare the data for anonymisation, anonymise the data and then apply certain post-processing methods and obtain validation of the selected anonymisation method.

Quick Start
----------

.. code-block:: bash

   pip install cdpg-anonkit --extra-index-url=https://test.pypi.org/simple/

.. code-block:: python

   import cdpg_anonkit
   
   # Quick example
   from cdpg_anonkit import SanitiseData as sanitisation

  example_data = pd.DataFrame({
        'age': [25, 40, 15, 60, 18, 90, 22, 45, 50, 55],
        'income': [50000, 80000, 65000, 120000, 20000, 90000, 55000, 75000, 85000, 95000],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack'],
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                 'New York', 'Chicago', 'Los Angeles', 'Dallas', 'Dallas']})
                 
  sanitisation_rules = {
    'age' : {'method': 'clip', 'params': {'min_value': 25, 'max_value': 70}},
    'name' : {'method': 'hash', 'params': {'salt': 'md5'}},
  }

  sanitised_data = sanitisation.sanitise_data(df=data_test, 
                                              columns_to_sanitise=['age', 'name'], 
                                              sanitisation_rules=sanitisation_rules)



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