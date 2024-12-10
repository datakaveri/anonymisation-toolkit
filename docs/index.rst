
.. rst-class:: hide-header

.. image:: _static/cdpg-logo_hires.png
    :align: center
    :width: 700px
    :target: https://dataforpublicgood.org.in
========================================
(Center of) Data for Public Good Anonkit
========================================

CDPG Anonkit is a toolkit that can be used to preprocess, anonymise, and post-process data. This toolkit was originally written as an application intended to be run inside a Trusted Execution Environment (TEE) and was later developed into a python package to allow anyone to be able to use it for any dataset.

.. code-block:: bash

  pip install cdpg-anonkit --extra-index-url=https://test.pypi.org/simple/

.. code-block:: python

   import cdpg_anonkit
   import pandas as pd
   
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


Contents
--------

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   intro
   quickstart
   api
   examples
   contributing
   changelog

Index
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`