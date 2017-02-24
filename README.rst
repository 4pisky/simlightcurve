simlightcurve
=============

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |travis|
    * - coverage
      - |coverage|
    * - package
      - |version|

Work in progress
----------------
The aim for this project is a collection of functions
('models', if you like, although they're rather simplified ones) that can
be used to fit the lightcurves of astronomical transients.
The feature-set we're aiming for are as follows:

* A well-documented and consistent interface, so it's easy for end-users to
install and get started.
* Well-referenced - whenever appropriate, links to the papers defining the
function are provided.
* Performant - lightcurve evaluations should be as fast as possible to enable
use on large data-sets, or under MCMC evaluation, etc. Initially this means
writing numpy-evaluated functions, in the long run it may mean exploration of
alternative optimizations [#]_.
* Make use of the astropy.modeling package, to leverage existing functionality
there.
* Minimal - just the functions and perhaps the basic fitting functionality from
astropy are provided - this package is 'agnostic' about how the lightcurves are
used to analyse data, which should make it more widely reusable [#]_.

.. [#]: We'll need to set up some benchmarks first of course.
.. [#]: We expect to develop a companion package that
utilises emcee to perform MCMC fitting of lightcurves to data, with
accompanying parameter posterior distributions.



.. |docs| image:: https://readthedocs.org/projects/simlightcurve/badge/?style=flat
    :target: https://readthedocs.org/projects/simlightcurve
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/4pisky/simlightcurve.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/4pisky/simlightcurve

.. |coverage| image:: https://codecov.io/github/4pisky/simlightcurve/branch/master/graph/badge.svg
    :alt: Test-coverage
    :target: https://codecov.io/github/4pisky/simlightcurve

.. |version| image:: https://img.shields.io/pypi/v/simlightcurve.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/simlightcurve