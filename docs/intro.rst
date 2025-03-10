Introduction
============

CDPG Anonkit is a toolkit that can be used to preprocess, anonymise, and post-process data. This toolkit was originally written as an application intended to be run inside a Trusted Execution Environment (TEE) and was later developed into a python package to allow anyone to be able to use it for any dataset.

Using the toolkit, you can perform the following operations:

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
.. * Differential Privacy
..     * Sensitivity Computation
..     * Noise Addition
.. * Post Processing 
..     * Rounding and Clipping
..     * Epsilon vs MAE


Installation
------------
CDPG Anonkit is available on PyPI. We recommend using the latest version of Python - CDPG Anonkit supports Python 3.10 and newer. 
We also recommend using a `virtual environment`_ in order
to isolate your project dependencies from other projects and the system.

.. _virtual environment: https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments

Install the most recent cdpg-anonkit version using pip:

.. code-block:: bash

    $ pip install cdpg-anonkit


Dependencies
~~~~~~~~~~~~

These will be installed automatically when installing the package.

-   `H3`_ A system to partition geographical areas into uniquely identifiable, hexagonal, hierarchical cells.

-   `Pandas`_ A library for high-performance, easy-to-use data structures and data analysis tools.

-   `Numpy`_ A package for scientific computing in python.

-   `typing_extensions`_ A complementary library to the standarding typing module. Enables run-time support for type hints.

.. _H3: https://docs.kepler.gl/docs/user-guides/c-types-of-layers/j-h3

.. _Pandas: https://pandas.pydata.org/docs/

.. _Numpy: https://numpy.org/doc/stable/

.. _typing_extensions: https://typing-extensions.readthedocs.io/en/latest/

Developer Dependencies
~~~~~~~~~~~~~~~~~~~~~~

These distributions will not be installed automatically and will only be installed on installing the dev version of cdpg-anonkit.

-   `Pytest`_ provides translation support in templates.

.. _Pytest: https://docs.pytest.org/en/stable/contents.html