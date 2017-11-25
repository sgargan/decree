========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/decree/badge/?style=flat
    :target: https://readthedocs.org/projects/decree
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/sgargan/decree.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/sgargan/decree

.. |codecov| image:: https://codecov.io/github/sgargan/decree/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/sgargan/decree

.. |version| image:: https://img.shields.io/pypi/v/decree.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/decree

.. |commits-since| image:: https://img.shields.io/github/commits-since/sgargan/decree/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/sgargan/decree/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/decree.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/decree

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/decree.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/decree

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/decree.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/decree


.. end-badges

Command pattern goodness..

* Free software: MIT license

Installation
============

::

    pip install decree

Documentation
=============

https://decree.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
