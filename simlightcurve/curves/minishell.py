from __future__ import absolute_import
import numpy as np
import scipy.optimize
from simlightcurve.lightcurve import (DictReprMixin,LightcurveBase,
                                      PeakSolverMixin,RiseTimeBisectMixin)


class Minishell(PeakSolverMixin, RiseTimeBisectMixin, LightcurveBase,
            DictReprMixin):
    """
    Supernova radio-lightcurve model (Type-II).

    Following VAST memo #3, Ryder 2010
    ( http://www.physics.usyd.edu.au/sifa/vast/uploads/Main/vast_memo3.pdf )
    """

    def __init__(self, k1, k2, k3, beta, delta1, delta2,
                 peak_search_t_start=1e7):
        super(Minishell,self).__init__()
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.beta = beta
        self.delta1 = delta1
        self.delta2 = delta2

        self._peak_solver_x0 = peak_search_t_start

    def _flux(self, t_offset):
        t_off_days = t_offset / (24*3600.)
        factor_evolve = self.k1 * np.power(t_off_days, self.beta)
        tau_csm_homog = self.k2 * np.power(t_off_days, self.delta1)
        factor_tau_external = np.exp(-tau_csm_homog)
        tau_csm_clump = self.k3 * np.power(t_off_days, self.delta2)
        factor_tau_csm_clump = (1 - np.exp(-tau_csm_clump) ) / tau_csm_clump
        return factor_evolve*factor_tau_external*factor_tau_csm_clump

    @property
    def t_offset_min(self):
        return 0.

    @property
    def t_offset_max(self):
        #We can do better, if necessary... but this is fine for now.
        return float('inf')

