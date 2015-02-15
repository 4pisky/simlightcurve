"""
Various lightcurves that break up into two models for rise and decay segments.
"""
from __future__ import absolute_import, division
import numpy as np
from astropy.modeling import FittableModel, Parameter, format_input
from simlightcurve.curves.powerlaw import Powerlaw


class LinearExp(FittableModel):
    inputs=('t',)
    outputs=('flux',)

    rise_time = Parameter()
    decay_tau = Parameter()
    amplitude = Parameter()
    t0 = Parameter(default=0.)


    @staticmethod
    def eval(t,
             rise_time,
             decay_tau,
             amplitude,
             t0):
        if np.ndim(t)==0:
            t=np.asarray(t,dtype=np.float).reshape((1,))
        t_offset = t-t0
        vals = np.zeros_like(t_offset,dtype=np.float)
        rise_idx = np.logical_and(t_offset >= -rise_time, t_offset <= 0)
        fall_idx = t_offset > 0
        vals[rise_idx] = (1 + t_offset[rise_idx]/rise_time)
        vals[fall_idx] = np.exp(-t_offset[fall_idx]/decay_tau)
        return amplitude*vals


    @format_input
    def __call__(self, t):
        return self.eval(t, *self.param_sets)



class GaussExp(FittableModel):
    inputs=('t',)
    outputs=('flux',)

    rise_tau = Parameter()
    decay_tau = Parameter()
    amplitude = Parameter()
    t0 = Parameter(default=0.)


    @staticmethod
    def eval(t,
             rise_tau,
             decay_tau,
             amplitude,
             t0):
        if np.ndim(t)==0:
            t=np.asarray(t,dtype=np.float).reshape((1,))
        t_offset = t-t0
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
    def __call__(self, t):
        return self.eval(t, *self.param_sets)

class GaussPowerlaw(FittableModel):
    inputs=('t',)
    outputs=('flux',)

    amplitude = Parameter()
    rise_tau = Parameter()
    decay_alpha = Parameter()
    decay_offset = Parameter(default=-1.0)
    t0 = Parameter(default=0.)


    @staticmethod
    def eval(t, amplitude, rise_tau,
             decay_alpha, decay_offset,
             t0):
        t_offset = t-t0
        vals = np.zeros_like(t_offset,dtype=np.float)
        #NB vals outside offset_min/max limits taken care of by LightcurveBase
        rise_idx = t_offset <= 0.
        fall_idx = t_offset > 0.
        vals[rise_idx] = np.exp(-1. * t_offset[rise_idx] * t_offset[rise_idx] /
                                (2. * rise_tau * rise_tau))

        pl_multiplier = 1.0/(decay_offset**decay_alpha)
        vals[fall_idx] = Powerlaw.eval(t_offset[fall_idx],
                                       init_amp=pl_multiplier,
                                       alpha_one=decay_alpha,
                                       t_offset_min=decay_offset,
                                       t0=-1.0*decay_offset)
        return amplitude*vals

    @format_input
    def __call__(self, t):
        return self.eval(t, *self.param_sets)
