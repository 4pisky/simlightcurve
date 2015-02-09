from __future__ import absolute_import



###########################################################
# Versioning; see also
# http://stackoverflow.com/questions/17583443
###########################################################
import os
from pkg_resources import get_distribution, DistributionNotFound
_dist_name = 'simlightcurve'
try:
    _dist = get_distribution(_dist_name)
    #The version number according to Pip:
    _nominal_version = _dist.version
    if not __file__.startswith(os.path.join(_dist.location, _dist_name)):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    #The actual copy in use if a custom PYTHONPATH or local dir import is used
    __version__ = 'Local import @ '+os.path.dirname(os.path.abspath(__file__))
else:
    __version__ = _nominal_version

