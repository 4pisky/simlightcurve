from __future__ import absolute_import
import datetime
from datetime import timedelta
from unittest import TestCase
import math

import simlightcurve.curves as simlc


class TestRyderCurve(TestCase):
    def shortDescription(self):
        return None

    def setUp(self):
        self.lc = simlc.Minishell(k1=2.5e2, k2=1.38e2, k3=1.47e5, beta=-1.5,
                                           delta1=-2.56, delta2=-2.69)
    def test_instantiation(self):
        self.assertEqual(self.lc.flux(0),0.0)

    def test_peak_flux_and_rise_time(self):
        lc = self.lc

        # Can't think of anything more sensible for now...
        self.assertTrue(lc.peak_flux > 0.0)
        self.assertLessEqual(lc.peak_flux , 10.0)

        half_peak_flux = 0.5 * lc.peak_flux
        half_peak_rise_time = lc.find_rise_t_offset(half_peak_flux)
        self.assertTrue(half_peak_rise_time < lc.peak_t_offset)
        self.assertTrue(half_peak_rise_time > lc.t_offset_min)
        self.assertAlmostEqual(lc.flux(half_peak_rise_time), 0.5*lc.peak_flux)