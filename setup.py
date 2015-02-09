#!/usr/bin/env python

from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="simlightcurve",
    version="alpha1",
    packages=['simlightcurve', 'simlightcurve.tests'], 
    description="Simple simulated lightcurve generation",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/simlightcurve",
    install_requires=required,
    test_suite='simlightcurve.tests'
)
