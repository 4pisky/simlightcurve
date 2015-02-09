from __future__ import absolute_import
import datetime
from datetime import timedelta
from unittest import TestCase
import numpy as np

from simlightcurve.curves import Powerlaw, OffsetPowerlaw


class TestPowerlawCurve(TestCase):
    def shortDescription(self):
        return None

    def test_linear_no_breaks(self):
        """
        Test the basic interface all works for a simple case.
        """
        lc = Powerlaw(init_amp=1, init_alpha=1)
        # Check negative handled by LightcurveBase
        self.assertEqual(lc.flux(-1), 0.0)
        self.assertEqual(lc.flux(1.0), 1.0)
        input_list = range(100)
        for posn in input_list:
            self.assertEqual(posn, lc.flux(posn))

        input_array = np.arange(0, 100, np.pi)
        out_array = lc.flux(input_array)
        self.assertTrue((input_array == out_array).all())

    def test_break(self):
        """
        Check that the break handling works as expected, for the simplest
        case where we maintain a linear slope.
        """
        lc = Powerlaw(init_amp=1, init_alpha=1,
                      breaks={1.0: 1.})

        # Check negative handled by LightcurveBase
        self.assertEqual(lc.flux(-1), 0.0)

        input_array = np.arange(0, 100, np.pi)
        out_array = lc.flux(input_array)
        self.assertTrue((input_array == out_array).all())


class TestPowerlawValueSolvers(TestCase):
    def setUp(self):
        self.lc = Powerlaw(init_amp=1.0, init_alpha=1,
                           breaks = {
                               1.0: -2
                           })

    def test_peak_flux(self):
        self.assertAlmostEqual(self.lc.peak_flux, 1.0)
        self.assertAlmostEqual(self.lc.peak_t_offset, 1.0)

    def test_find_rise_t_offset(self):
        lc = self.lc
        half_peak_flux  =0.5*lc.peak_flux
        half_peak_rise_time = lc.find_rise_t_offset(half_peak_flux)
        self.assertAlmostEqual(half_peak_rise_time,0.5)

class TestOffsetPowerlawCurve(TestCase):
    def shortDescription(self):
        return None

    def test_linear_no_breaks(self):
        """
        Test the basic interface all works for a simple case.
        """
        lc = OffsetPowerlaw(init_amp=1, init_alpha=1, flux_offset=-1)
        # Check negative handled by LightcurveBase
        self.assertEqual(lc.flux(-1), 0.0)
        self.assertEqual(lc.flux(1.0), 1.0)
        input_list = range(100)
        for posn in input_list:
            self.assertEqual(posn, lc.flux(posn))

        input_array = np.arange(0, 100, np.pi)
        out_array = lc.flux(input_array)
        self.assertTrue((input_array == out_array).all())

    def test_break(self):
        """
        Check that the break handling works as expected, for the simplest
        case where we maintain a linear slope.
        """
        lc = OffsetPowerlaw(init_amp=1, init_alpha=1, flux_offset=-1,
                      breaks={1.0: 1.})

        # Check negative handled by LightcurveBase
        self.assertEqual(lc.flux(-1), 0.0)

        input_array = np.arange(0, 100, np.pi)
        out_array = lc.flux(input_array)
        self.assertTrue((input_array == out_array).all())


class TestOffsetPowerlawValueSolvers(TestCase):
    def setUp(self):
        self.lc = OffsetPowerlaw(init_amp=1.0, init_alpha=1, flux_offset=-1,
                           breaks = {
                               1.0: -2
                           })

    def test_peak_flux(self):
        self.assertAlmostEqual(self.lc.peak_flux, 1.0)
        self.assertAlmostEqual(self.lc.peak_t_offset, 1.0)

    def test_find_rise_t_offset(self):
        lc = self.lc
        half_peak_flux  =0.5*lc.peak_flux
        half_peak_rise_time = lc.find_rise_t_offset(half_peak_flux)
        self.assertAlmostEqual(half_peak_rise_time,0.5)
