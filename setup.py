#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

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
