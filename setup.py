#!/usr/bin/env python

from setuptools import setup, find_packages

required=['scipy',
          'astropy',
          ]


setup(
    name="simlightcurve",
    version="0.1a1",
    packages=find_packages(),
    description="Simple simulated lightcurve generation",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/simlightcurve",
    install_requires=required,
    test_suite='simlightcurve.tests'
)
