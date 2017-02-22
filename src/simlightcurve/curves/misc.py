from __future__ import absolute_import
import numpy as np
from astropy.modeling import (
    FittableModel, Parameter)
from astropy.modeling.models import custom_model

@custom_model
def logistic_rise(t, amplitude=1.0, t0=0.0):
    return 1.0 / (1.0 + np.exp(-( t-t0) / amplitude))

@custom_model
def logistic_drop(t, amplitude=1.0,t0=0.0):
    return 1.0 - logistic_rise.evaluate(t, amplitude, t0)

@custom_model
def softplus_drop(t, amplitude=1.0, t0=0.0):
    return 1.0 / (1.0 + np.exp(-(t - t0) / amplitude))


class NegativeQuadratic(FittableModel):
    """
    Very simple example, used for testing purposes.
    """

    inputs=('t',)
    outputs=('flux',)
    amplitude=Parameter()
    t0=Parameter(default=0.0)

    @staticmethod
    def evaluate(t, amplitude, t0):
        if np.ndim(t)==0:
            t=np.asarray(t,dtype=np.float).reshape((1,))
        t_offset = t-t0
        root = np.sqrt(amplitude)
        t_valid = (t_offset > -root)& (t_offset < root)
        # print "t_offset", t_offset
        # print "T_valid", t_valid
        vals = np.zeros_like(t_offset)
        vals[t_valid] = amplitude - t_offset[t_valid]**2
        return vals
        # return amplitude - t_offset**2
