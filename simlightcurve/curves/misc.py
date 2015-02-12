from __future__ import absolute_import
import numpy as np
from astropy.modeling import (
    FittableModel, Parameter, format_input)
from astropy.modeling.models import custom_model_1d

@custom_model_1d
def logistic_rise(t_offset, loc=0.0, scale=1.0):
    return 1.0 / (1.0 + np.exp(-(t_offset - loc) / scale))

@custom_model_1d
def logistic_drop(t_offset, loc=0.0, scale=1.0):
    return 1.0 - logistic_rise(t_offset, loc, scale)

@custom_model_1d
def softplus_drop(t_offset, loc=0.0, scale=1.0):
    return 1.0 / (1.0 + np.exp(-(t_offset - loc) / scale))


class NegativeQuadratic(FittableModel):
    """
    Very simple example, used for testing purposes.
    """

    inputs=('t_offset',)
    outputs=('flux',)
    amplitude=Parameter()

    @staticmethod
    def eval(t_offset, amplitude):
        if np.ndim(t_offset)==0:
            t_offset=np.asarray(t_offset,dtype=np.float).reshape((1,))
        root = np.sqrt(amplitude)
        t_valid = (t_offset > -root)& (t_offset < root)
        # print "t_offset", t_offset
        # print "T_valid", t_valid
        vals = np.zeros_like(t_offset)
        vals[t_valid] = amplitude - t_offset[t_valid]**2
        return vals
        # return amplitude - t_offset**2


    @format_input
    def __call__(self, t_offset):
        return self.eval(t_offset, *self.param_sets)