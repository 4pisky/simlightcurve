from __future__ import absolute_import
import datetime
from datetime import timedelta
from unittest import TestCase
import math

import simlightcurve.curves as simlc


class TestSimpleModSigmoidExpCurve(TestCase):
    def shortDescription(self):
        return None

    def setUp(self):
        """Test basic b=0 case"""
        hr = 60. * 60.
        self.decay_tau = 24 * hr
        self.rise_tau = self.decay_tau / 10
        self.t1_offset = 0.5 * self.decay_tau
        self.rawlc = simlc.ModSigmoidExp(a=1., b=0, t1_minus_t0=0.0,
                                  rise_tau=self.rise_tau,
                                  decay_tau=self.decay_tau, )

    def test_raw_values(self):
        self.assertAlmostEqual(self.rawlc.flux(0), 0.5)
        # Still rising after zero-point in un-normalised curve:
        self.assertTrue(self.rawlc.flux(0) < self.rawlc.flux(60))

    def test_origin_flux_value(self):
        self.assertAlmostEqual(self.rawlc.flux(0), 0.5)

    def test_peak_flux_and_rise_time(self):
        lc = self.rawlc

        # Can't think of anything more sensible for now...
        self.assertTrue(lc.peak_flux > 0.0)
        self.assertTrue(lc.peak_flux < 10.0)

        half_peak_flux = 0.5 * lc.peak_flux
        half_peak_rise_time = lc.find_rise_t_offset(half_peak_flux)
        self.assertTrue(half_peak_rise_time < lc.peak_t_offset)
        self.assertTrue(half_peak_rise_time > lc.t_offset_min)
        self.assertAlmostEqual(lc.flux(half_peak_rise_time), 0.5*lc.peak_flux)

class TestNormedModSigmoidExpCurve(TestCase):
    def shortDescription(self):
        return None

    def setUp(self):
        hr = 60. * 60.
        self.decay_tau = 24 * hr
        self.rise_tau = self.decay_tau / 10
        self.t1_offset = 0.5 * self.decay_tau
        self.peak= 1.
        self.lc = simlc.NormedModSigmoidExp(peak_flux=self.peak, b=0, t1_minus_t0=0.0,
                                           rise_tau=self.rise_tau,
                                           decay_tau=self.decay_tau, )


    def test_normed_flux_values(self):
        """Check normalisation works correctly in basic b=0 case"""
        lc = self.lc
        self.assertAlmostEqual(lc.flux(0), 1.0)
        # Check (crudely) that it's really a peak
        self.assertTrue(lc.flux(0) > lc.flux(1))
        self.assertTrue(lc.flux(0) > lc.flux(-1))
        self.assertTrue(lc.flux(0) > lc.flux(1000))
        self.assertTrue(lc.flux(0) > lc.flux(-1000))

    def test_peak_flux(self):
        self.assertEqual(self.lc.flux([0]), 1)
        self.assertEqual(self.lc.peak_flux, 1)
        self.assertEqual(self.lc.peak_t_offset, 0.0)

    def test_find_rise_t_offset(self):
        half_peak_rise_time = self.lc.find_rise_t_offset(0.5*self.peak)
        # print half_peak_rise_time
        self.assertTrue(half_peak_rise_time<0)
        self.assertAlmostEqual(self.lc.flux(half_peak_rise_time), 0.5*self.peak)
        self.assertEqual(self.lc.find_rise_t_offset(1.5*self.peak), None)
