from __future__ import absolute_import
import math
import numpy as np
from simlightcurve.lightcurve import LightcurveBase


def logistic_rise(t_offset, loc=0.0, scale=1.0):
    return 1.0 / (1.0 + np.exp(-(t_offset - loc) / scale))

def logistic_drop(t_offset, loc=0.0, scale=1.0):
    return 1.0 - logistic_rise(t_offset, loc, scale)

def softplus_drop(t_offset, loc=0.0, scale=1.0):
    return 1.0 / (1.0 + np.exp(-(t_offset - loc) / scale))



class Null(LightcurveBase):
    """
    Returns zero flux at all times.
    """
    def __init__(self):
        super(Null, self).__init__()

    def _flux(self, t_offset):
        return np.zeros_like(t_offset)

    @property
    def t_offset_min(self):
        return 0.

    @property
    def t_offset_max(self):
        return 0.

    def peak_flux(self):
        return 0.

    def peak_t_offset(self):
        return 0

    def find_rise_t_offset(self, threshold):
        return None



class NegativeQuadratic(LightcurveBase):
    """
    Very simple example, used for testing purposes.
    """

    def __init__(self, peak):
        super(NegativeQuadratic, self).__init__()
        self._peak_flux = peak
        self.root = math.sqrt(peak)

    def _flux(self, t_offset):
        return self._peak_flux - t_offset ** 2

    @property
    def t_offset_min(self):
        return -self.root

    @property
    def t_offset_max(self):
        return self.root

    @property
    def peak_flux(self):
        return self._peak_flux

    @property
    def peak_t_offset(self):
        return 0.

    def find_rise_t_offset(self, threshold):
        if threshold>self._peak_flux:
            return None
        return -(math.sqrt(self._peak_flux - threshold))