from __future__ import absolute_import
from unittest import TestCase

import numpy as np

from simlightcurve.curves import NegativeQuadratic
from simlightcurve.solvers import find_peak, find_rise_t

class TestSolversOnQuadratic(TestCase):
    def setUp(self):
        self.peak = 10
        self.lc = NegativeQuadratic(amplitude=self.peak, t0=None)

    def test_input_output_dim_handling(self):
        lc = self.lc
        self.assertEqual(lc(0),self.peak)
        self.assertEqual(lc(np.asarray(0)),self.peak)
        self.assertEqual(lc([0]),[self.peak])
        self.assertTrue( (lc([0,1]) == [self.peak,self.peak-1]).all())

    def test_input_domain_handling(self):
        lc = self.lc
        #Cleaned values are non-negative
        self.assertEqual(lc(100),0)
        self.assertEqual(lc(-100),0)

    def test_peak_flux(self):
        peak_t, peak_f = find_peak(self.lc, t_init=1.0)
        self.assertEqual(peak_f, self.peak)

    def test_find_rise_t_offset(self):
        rise_t = find_rise_t(self.lc, threshold=self.peak-1,
                                    t_min=-5, t_max=0)
        self.assertAlmostEqual(rise_t, -1.)