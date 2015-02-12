"""
Various lightcurves that break up into two models for rise and decay segments.
"""
from __future__ import absolute_import, division
import numpy as np
from astropy.modeling import FittableModel, Parameter, format_input
# from simlightcurve.curves.powerlaw import OffsetPowerlaw


class LinearExp(FittableModel):
    
    inputs=('t_offset',)
    outputs=('flux',)

    rise_time = Parameter()
    decay_tau = Parameter()
    amplitude = Parameter()


    @staticmethod
    def eval(t_offset,
             rise_time,
             decay_tau,
             amplitude):
        if np.ndim(t_offset)==0:
            t_offset=np.asarray(t_offset,dtype=np.float).reshape((1,))
        vals = np.zeros_like(t_offset,dtype=np.float)
        rise_idx = np.logical_and(t_offset >= -rise_time, t_offset <= 0)
        fall_idx = t_offset > 0
        vals[rise_idx] = (1 + t_offset[rise_idx]/rise_time)
        vals[fall_idx] = np.exp(-t_offset[fall_idx]/decay_tau)
        return amplitude*vals


    @format_input
    def __call__(self, t_offset):
        return self.eval(t_offset, *self.param_sets)



class GaussExp(FittableModel):

    inputs=('t_offset',)
    outputs=('flux',)

    rise_tau = Parameter()
    decay_tau = Parameter()
    amplitude = Parameter()

    @staticmethod
    def eval(t_offset,
             rise_tau,
             decay_tau,
             amplitude):
        if np.ndim(t_offset)==0:
            t_offset=np.asarray(t_offset,dtype=np.float).reshape((1,))
        vals = np.zeros_like(t_offset,dtype=np.float)
        #NB vals outside offset_min/max limits taken care of by LightcurveBase
        rise_idx = t_offset <= 0.
        fall_idx = t_offset > 0.
        vals[rise_idx] = np.exp( -1.*t_offset[rise_idx]*t_offset[rise_idx] /
                                 (2.*rise_tau*rise_tau)
                                )
        vals[fall_idx] = np.exp(-t_offset[fall_idx]/decay_tau)
        return amplitude*vals


    @format_input
    def __call__(self, t_offset):
        return self.eval(t_offset, *self.param_sets)

# class GaussPowerlaw(LightcurveBase,DictReprMixin):
#     """
#     NB peak finding routines assume powerlaw is truely decay, i.e. only negative
#     indices.
#     """
#     def __init__(self, peak_flux, rise_tau, init_alpha, breaks=None):
#         super(GaussPowerlaw,self).__init__()
#         _peak_flux = peak_flux
#         rise_tau = rise_tau
#
#         decay_curve = OffsetPowerlaw(init_amp=_peak_flux,
#                                     init_alpha=init_alpha,
#                                     flux_offset=0,
#                                     breaks=breaks)
#
#     def _flux(self, t_offset):
#         vals = np.zeros_like(t_offset,dtype=np.float)
#         #NB vals outside offset_min/max limits taken care of by LightcurveBase
#         rise_idx = t_offset <= 0.
#         fall_idx = t_offset > 0.
#         vals[rise_idx] = (_peak_flux*
#             np.exp( -1.*t_offset[rise_idx]*t_offset[rise_idx] /
#                      (2.*rise_tau*rise_tau))
#         )
#         vals[fall_idx] = decay_curve.flux(t_offset[fall_idx])
#         return vals