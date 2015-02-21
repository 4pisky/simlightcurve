from __future__ import absolute_import, division
import numpy as np
from astropy.modeling import FittableModel, Parameter
from simlightcurve.curves.powerlaw import Powerlaw


class GaussExp(FittableModel):
    inputs=('t',)
    outputs=('flux',)

    amplitude = Parameter()
    rise_tau = Parameter()
    decay_tau = Parameter()
    t0 = Parameter(default=0.)


    @staticmethod
    def evaluate(t,
             amplitude,
             rise_tau,
             decay_tau,
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


