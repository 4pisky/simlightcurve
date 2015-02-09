from __future__ import absolute_import, division
import numpy as np

from simlightcurve.lightcurve import (DictReprMixin, LightcurveBase,
                                      PeakSolverMixin,RiseTimeBisectMixin)


def modsigmoidexp_func(a, b,
                  t1_minus_t0,
                  rise_tau, decay_tau,
                  t0_offset):
    """
    Supernova optical-lightcurve function, parameterisable to all SNe types.

    Following Karpenka et al 2012; Eq 1.
    ( http://adsabs.harvard.edu/abs/2013MNRAS.429.1278K )
    """
    t_minus_t1 = t0_offset - t1_minus_t0
    b_fac = 1 + b * t_minus_t1*t_minus_t1
    #NB imported 'truediv' behaviour, so OK even if t0, decay both integers.
    exp_num = np.exp(-t0_offset / decay_tau)
    exp_denom = 1 + np.exp(-t0_offset / rise_tau)
    return a*b_fac*exp_num/exp_denom


class ModSigmoidExp(PeakSolverMixin,RiseTimeBisectMixin,
               LightcurveBase,DictReprMixin):
    """
    Supernova optical-lightcurve model, applicable to all SNe types.

    Following Karpenka et al 2012; Eq 1.
    ( http://adsabs.harvard.edu/abs/2013MNRAS.429.1278K )
    """
    def __init__(self, a, b, t1_minus_t0, rise_tau, decay_tau):
        super(ModSigmoidExp,self).__init__()
        self.a = a
        self.b = b
        self.t1_minus_t0 = t1_minus_t0
        self.rise_tau = rise_tau
        self.decay_tau = decay_tau
        self._peak_solver_x0 = 0.


    def _flux(self, t_offset):
        return modsigmoidexp_func(a=self.a, b=self.b,
                             t1_minus_t0=self.t1_minus_t0,
                             rise_tau=self.rise_tau,
                             decay_tau=self.decay_tau,
                             t0_offset=t_offset
                             )

    @property
    def t_offset_min(self):
        return -10.*self.rise_tau
    @property
    def t_offset_max(self):
        return 10.*self.decay_tau



class NormedModSigmoidExp(RiseTimeBisectMixin,LightcurveBase, DictReprMixin):
    """
    Convenience wrapper, renormalises the ModulatedSigmoid curve.
    For convenience, we perform a per-instance fitting & re-parameterization
    to obtain a curve with the desired peak flux, with the ``flux`` function
    taking a time offset parameter **relative to this time of peak flux**.

    """

    def __init__(self, peak_flux, b, t1_minus_t0, rise_tau, decay_tau ):
        """

        """
        super(NormedModSigmoidExp, self).__init__()

        self.raw = ModSigmoidExp(a=1.0, b=float(b),
                            t1_minus_t0=float(t1_minus_t0),
                            rise_tau=rise_tau, decay_tau=decay_tau)

        self.norm = peak_flux / self.raw.peak_flux
        self._peak_flux = peak_flux

    def _flux(self, t_offset):
        """
        Returns flux value at seconds_offset from peak flux
        For convenience
        """
        return (self.norm *
                self.raw.flux(t_offset + self.raw.peak_t_offset))

    @property
    def t_offset_min(self):
        return self.raw.t_offset_min

    @property
    def t_offset_max(self):
        return self.raw.t_offset_max

    @property
    def peak_flux(self):
        return self._peak_flux

    @property
    def peak_t_offset(self):
        return 0.
