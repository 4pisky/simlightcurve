#!/usr/bin/env python

from setuptools import setup, find_packages

import versioneer

install_requires = ['numpy',
                    'scipy',
                    'astropy',
                    # Only need for doc-plots, but we unit-test these:
                    'matplotlib',
                    'seaborn',
                    ]

test_requires = [
    'pytest>3',
    'coverage'
]

extras_require = {
    'test': test_requires,
    'all': test_requires
}

setup(
    name="simlightcurve",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    description="Simple simulated lightcurve generation",
    author="Tim Staley",
    author_email="github@timstaley.co.uk",
    url="https://github.com/timstaley/simlightcurve",
    install_requires=install_requires,
)
