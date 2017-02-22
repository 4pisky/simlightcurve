from __future__ import absolute_import



###########################################################
# Versioning; see also
# http://stackoverflow.com/questions/17583443
###########################################################
import os

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
