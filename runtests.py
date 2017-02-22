#!/usr/bin/env python
"""
A small wrapper around pytest

Can be used to configure logging while running the tests.
"""
import sys
import pytest

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(pytest.main())
