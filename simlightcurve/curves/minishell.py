from __future__ import absolute_import
import numpy as np

from astropy.modeling import FittableModel, Parameter, format_input

class Minishell(FittableModel):
    """
    Supernova radio-lightcurve model (Type-II).

    CF
    K. Weiler et al, 2002:
    http://www.annualreviews.org/doi/abs/10.1146/annurev.astro.40.060401.093744

    and VAST memo #3, Ryder 2010:
    http://www.physics.usyd.edu.au/sifa/vast/uploads/Main/vast_memo3.pdf

    See Weiler et al for some typical parameter values.
    """
    inputs=('t',)
    outputs=('flux',)

    k1 = Parameter()
    k2 = Parameter()
    k3 = Parameter()
    beta = Parameter()
    delta1 = Parameter()
    delta2 = Parameter()
    t0 = Parameter(default=0.)

    @staticmethod
    def _curve(t_offset,k1,k2,k3,beta,delta1,delta2):
        """
        Internal function that is only valid at t > 0
        """
        factor_evolve = k1 * np.power(t_offset, beta)
        tau_csm_homog = k2 * np.power(t_offset, delta1)
        factor_tau_external = np.exp(-tau_csm_homog)
        tau_csm_clump = k3 * np.power(t_offset, delta2)
        factor_tau_csm_clump = (1 - np.exp(-tau_csm_clump) ) / tau_csm_clump
        return factor_evolve*factor_tau_external*factor_tau_csm_clump

    @staticmethod
    def eval(t,k1,k2,k3,beta,delta1,delta2,t0):
        """
        Wraps _curve function to only process values at t > 0
        """
        t_offset = t-t0
        vals = np.zeros_like(t_offset,dtype=np.float)
        t_valid = ( t_offset > 0 )
        vals[t_valid] = Minishell._curve(t_offset[t_valid],k1,k2,k3,beta,delta1,delta2)
        return vals

    @format_input
    def __call__(self, t):
        return self.eval(t, *self.param_sets)