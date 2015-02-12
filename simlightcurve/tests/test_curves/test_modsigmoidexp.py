from __future__ import absolute_import
from unittest import TestCase

from simlightcurve.curves import ModSigmoidExp
from simlightcurve.solvers import find_peak, find_rise_t_offset

class TestSimpleModSigmoidExpCurve(TestCase):
    def shortDescription(self):
        return None

    def setUp(self):
        """Test basic b=0 case"""
        self.decay_tau = 24
        self.rise_tau = self.decay_tau / 10
        self.t1_offset = 0.5 * self.decay_tau
        self.lc = ModSigmoidExp(a=1., b=0,
                                t1_minus_t0=0.0,
                               rise_tau=self.rise_tau,
                               decay_tau=self.decay_tau, )

    def test_values(self):
        self.assertAlmostEqual(self.lc(0), 0.5)
        # Still rising after zero-point
        self.assertTrue(self.lc(0) < self.lc(1))

    def test_origin_flux_value(self):
        self.assertAlmostEqual(self.lc(0), 0.5)


    def test_solvers(self):
        lc = self.lc
    #     # Can't think of anything more sensible for now...
        peak_t_offset, peak_flux = find_peak(lc,t_init=0)
        self.assertTrue(peak_flux > 0.0)
        self.assertTrue(peak_flux < 10.0)

        # print( "Peak:",peak_t_offset,peak_flux)
        half_peak_flux = 0.5 * peak_flux

        t_early = -self.rise_tau*3

        half_peak_rise_time = find_rise_t_offset(lc, half_peak_flux,
                                 t_min=t_early, t_max=peak_t_offset)
        # print( "Half-rise time:",half_peak_rise_time)
        self.assertTrue(half_peak_rise_time < peak_t_offset)
        self.assertTrue(half_peak_rise_time > t_early)
        self.assertAlmostEqual(lc(half_peak_rise_time), 0.5*peak_flux)


