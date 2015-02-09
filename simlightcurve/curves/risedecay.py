"""
Various lightcurves that break up into two models for rise and decay segments.
"""
from __future__ import absolute_import, division
import numpy as np
from simlightcurve.lightcurve import DictReprMixin, LightcurveBase
from simlightcurve.curves.powerlaw import OffsetPowerlaw


class LinearExp(LightcurveBase, DictReprMixin):
    def __init__(self, rise_time, decay_tau, peak_flux):
        super(LinearExp,self).__init__()
        self.rise_time = rise_time
        self.decay_tau = decay_tau
        self._peak_flux = peak_flux

    def _flux(self, t_offset):
        vals = np.zeros_like(t_offset,dtype=np.float)
        #NB vals outside offset_min/max limits taken care of by LightcurveBase
        rise_idx = t_offset <= 0
        fall_idx = t_offset > 0
        vals[rise_idx] = (1 + t_offset[rise_idx]/self.rise_time)
        vals[fall_idx] = np.exp(-t_offset[fall_idx]/self.decay_tau)
        return self._peak_flux*vals

    @property
    def t_offset_min(self):
        return -self.rise_time

    @property
    def t_offset_max(self):
        #Use 10 e-folding times, i.e. when flux has dropped to < 5*10^-5
        return 10.0*self.decay_tau

    def peak_flux(self):
        return self._peak_flux

    def peak_t_offset(self):
        return 0.

    def find_rise_t_offset(self, threshold):
        if threshold>self._peak_flux:
            return None
        return -self.rise_time*threshold/self._peak_flux


class GaussExp(LightcurveBase, DictReprMixin):
    def __init__(self, rise_tau, decay_tau, peak_flux):
        super(GaussExp,self).__init__()
        self.rise_tau = rise_tau
        self.decay_tau = decay_tau
        self._peak_flux = peak_flux

    def _flux(self, t_offset):
        vals = np.zeros_like(t_offset,dtype=np.float)
        #NB vals outside offset_min/max limits taken care of by LightcurveBase
        rise_idx = t_offset <= 0.
        fall_idx = t_offset > 0.
        vals[rise_idx] = np.exp( -1.*t_offset[rise_idx]*t_offset[rise_idx] /
                                 (2.*self.rise_tau*self.rise_tau)
                                )
        vals[fall_idx] = np.exp(-t_offset[fall_idx]/self.decay_tau)
        return self._peak_flux*vals

    @property
    def t_offset_min(self):
        return -10.0*self.rise_tau

    @property
    def t_offset_max(self):
        #Use 10 e-folding times, i.e. when flux has dropped to < 5*10^-5
        return 10.0*self.decay_tau

    def peak_flux(self):
        return self._peak_flux

    def peak_t_offset(self):
        return 0.

    def find_rise_t_offset(self, threshold):
        if threshold>self._peak_flux:
            return None
        root_sq = -2.*self.rise_tau*self.rise_tau*np.log(threshold/self._peak_flux)
        return -1.*np.sqrt(root_sq)

class GaussPowerlaw(LightcurveBase,DictReprMixin):
    """
    NB peak finding routines assume powerlaw is truely decay, i.e. only negative
    indices.
    """
    def __init__(self, peak_flux, rise_tau, init_alpha, breaks=None):
        super(GaussPowerlaw,self).__init__()
        self._peak_flux = peak_flux
        self.rise_tau = rise_tau

        self.decay_curve = OffsetPowerlaw(init_amp=self._peak_flux,
                                    init_alpha=init_alpha,
                                    flux_offset=0,
                                    breaks=breaks)

    def _flux(self, t_offset):
        vals = np.zeros_like(t_offset,dtype=np.float)
        #NB vals outside offset_min/max limits taken care of by LightcurveBase
        rise_idx = t_offset <= 0.
        fall_idx = t_offset > 0.
        vals[rise_idx] = (self._peak_flux*
            np.exp( -1.*t_offset[rise_idx]*t_offset[rise_idx] /
                     (2.*self.rise_tau*self.rise_tau))
        )
        vals[fall_idx] = self.decay_curve.flux(t_offset[fall_idx])
        return vals

    @property
    def t_offset_min(self):
        return -10.0*self.rise_tau

    @property
    def t_offset_max(self):
        return self.decay_curve.t_offset_max

    def peak_flux(self):
        return self._peak_flux

    def peak_t_offset(self):
        return 0.

    def find_rise_t_offset(self, threshold):
        if threshold>self._peak_flux:
            return None
        root_sq = -2.*self.rise_tau*self.rise_tau*np.log(threshold/self._peak_flux)
        return -1.*np.sqrt(root_sq)