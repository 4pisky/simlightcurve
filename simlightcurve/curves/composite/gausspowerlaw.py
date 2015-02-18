from __future__ import absolute_import, division
import numpy as np
from astropy.modeling import FittableModel, Parameter, format_input
from simlightcurve.curves.powerlaw import Powerlaw



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
