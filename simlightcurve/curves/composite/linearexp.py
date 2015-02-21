from __future__ import absolute_import, division
import numpy as np
from astropy.modeling import FittableModel, Parameter


class LinearExp(FittableModel):
    inputs=('t',)
    outputs=('flux',)

    amplitude = Parameter()
    rise_time = Parameter()
    decay_tau = Parameter()
    t0 = Parameter(default=0.)


    @staticmethod
    def evaluate(t,
             amplitude,
             rise_time,
             decay_tau,
             t0
    ):
        if np.ndim(t)==0:
            t=np.asarray(t,dtype=np.float).reshape((1,))
        t_offset = t-t0
        vals = np.zeros_like(t_offset,dtype=np.float)
        rise_idx = np.logical_and(t_offset >= -rise_time, t_offset <= 0)
        fall_idx = t_offset > 0
        vals[rise_idx] = (1 + t_offset[rise_idx]/rise_time)
        vals[fall_idx] = np.exp(-t_offset[fall_idx]/decay_tau)
        return amplitude*vals


