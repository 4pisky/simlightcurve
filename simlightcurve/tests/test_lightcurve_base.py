from __future__ import absolute_import
from unittest import TestCase

import numpy as np

from simlightcurve.curves import NegativeQuadratic



class TestFluxFunction(TestCase):
    def setUp(self):
        self.peak = 10
        self.lc = NegativeQuadratic(self.peak)

    def test_input_output_dim_handling(self):
        lc = self.lc
        self.assertEqual(lc.flux(0),self.peak)
        self.assertEqual(lc.flux(np.asarray(0)),self.peak)
        self.assertEqual(lc.flux([0]),[self.peak])
        self.assertTrue( (lc.flux([0,1]) == [self.peak,self.peak-1]).all())

    def test_input_domain_handling(self):
        lc = self.lc
        #Raw values are negative
        self.assertTrue(lc._flux(100)<0)
        self.assertTrue(lc._flux(-100)<0)
        #Cleaned values are non-negative
        self.assertEqual(lc.flux(100),0)
        self.assertEqual(lc.flux(-100),0)

    def test_peak_flux(self):
        self.assertEqual(self.lc.peak_flux, self.peak)
    def test_find_rise_t_offset(self):
        self.assertEqual(self.lc.find_rise_t_offset(self.peak-1), -1.)