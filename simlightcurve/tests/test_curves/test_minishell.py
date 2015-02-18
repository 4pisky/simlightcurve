from __future__ import absolute_import
from unittest import TestCase
from simlightcurve.solvers import find_peak, find_rise_t

import simlightcurve.curves as simlc


class TestMinishellCurve(TestCase):
    def shortDescription(self):
        return None

    def setUp(self):
        self.lc = simlc.Minishell(k1=2.5e2, k2=1.38e2, k3=1.47e5, beta=-1.5,
                                           delta1=-2.56, delta2=-2.69)
    def test_instantiation(self):
        self.assertEqual(self.lc(0),0.0)

    def test_solvers(self):
        lc = self.lc
    #
    #     # Can't think of anything more sensible for now...
        peak_t_offset, peak_flux = find_peak(lc,t_init=1.0)
        self.assertTrue(peak_flux > 0.0)
        self.assertTrue(peak_flux < 10.0)
    #
        half_peak_flux = 0.5 * peak_flux
        half_peak_rise_time = find_rise_t(lc, half_peak_flux,
                                                 t_min=0, t_max=peak_t_offset)
        self.assertTrue(half_peak_rise_time < peak_t_offset)
        self.assertTrue(half_peak_rise_time > 0)
        self.assertAlmostEqual(lc(half_peak_rise_time), 0.5*peak_flux)
