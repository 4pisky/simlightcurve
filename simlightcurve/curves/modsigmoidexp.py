from __future__ import absolute_import, division
import numpy as np
from astropy.modeling import FittableModel, Parameter, format_input


class ModSigmoidExp(FittableModel):
    """
    Sigmoidal rise / exponential decay modulated by a quadratic polynomial.

    Typically applied as a supernova optical-lightcurve model,
    applicable to all SNe types.

    Following Karpenka et al 2012; Eq 1.
    ( http://adsabs.harvard.edu/abs/2013MNRAS.429.1278K )
    """
    inputs=('t',)
    outputs=('flux',)
    
    a = Parameter()
    b = Parameter()
    t1_minus_t0 = Parameter()
    rise_tau = Parameter()
    decay_tau = Parameter()
    t0 = Parameter(default=0.)


    @staticmethod
    def eval(t,
             a,
             b,
             t1_minus_t0,
             rise_tau,
             decay_tau,
             t0):
        t_offset = t - t0
        t_minus_t1 = t_offset - t1_minus_t0
        b_fac = 1 + b * t_minus_t1*t_minus_t1
        #NB imported 'truediv' behaviour, so OK even if t0, decay both integers.
        exp_num = np.exp(-t_offset / decay_tau)
        exp_denom = 1 + np.exp(-t_offset / rise_tau)
        return a*b_fac*exp_num/exp_denom

    @format_input
    def __call__(self, t):
        return self.eval(t, *self.param_sets)