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
* Differential Privacy
    * Sensitivity Computation
    * Noise Addition
* Post Processing 
    * Rounding and Clipping
    * Epsilon vs MAE


Installation
-----------
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

-   `MarkupSafe`_ escapes untrusted input when rendering templates to
    avoid injection attacks.

.. _MarkupSafe: https://markupsafe.palletsprojects.com/


Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

These distributions will not be installed automatically.

-   `Babel`_ provides translation support in templates.

.. _Babel: https://babel.pocoo.org/