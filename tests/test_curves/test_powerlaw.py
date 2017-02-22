from __future__ import absolute_import
from unittest import TestCase
import numpy as np

from simlightcurve.solvers import find_peak, find_rise_t
from simlightcurve.curves import (
    Powerlaw,
    SingleBreakPowerlaw,
#,OffsetPowerlaw
)


class TestPowerlawCurve(TestCase):
    def shortDescription(self):
        return None

    def test_linear_no_breaks(self):
        """
        Test the basic interface all works for a simple case.
        """
        lc = Powerlaw(init_amp=1, alpha_one=1, t_offset_min=None, t0=None)
        # Check negative handled by LightcurveBase
        self.assertEqual(lc(-1), 0.0)
        self.assertEqual(lc(1.0), 1.0)
        input_list = range(100)
        for posn in input_list:
            self.assertEqual(posn, lc(posn))

        input_array = np.arange(0, 100, np.pi)
        out_array = lc(input_array)
        self.assertTrue((input_array == out_array).all())

    def test_break(self):
        """
        Check that the break handling works as expected, for the simplest
        case where we maintain a linear slope.
        """
        lc = SingleBreakPowerlaw(init_amp=1,
                                 alpha_one=1.,
                                 break_one_t_offset=1.0,
                                 alpha_two=1.0,
                                 t_offset_min=None,
                                 t0=None)

        # Check negative handled
        self.assertEqual(lc(-1), 0.0)

        input_array = np.arange(0, 100, np.pi)
        out_array = lc(input_array)
        self.assertTrue((input_array == out_array).all())


class TestPowerlawValueSolvers(TestCase):
    def setUp(self):
        self.lc = SingleBreakPowerlaw(
            init_amp=1.0,
            alpha_one=1,
            break_one_t_offset=1.0,
            alpha_two=-2,
            t_offset_min=None,
            t0=None
        )
    #
    def test_peak_flux(self):
        self.assertAlmostEqual(self.lc(1), 1.0)
        peak_t_offset, peak_flux = find_peak(self.lc, t_init=0)
        self.assertAlmostEqual(peak_t_offset, 1.0)
        self.assertAlmostEqual(peak_flux, 1.0)

    def test_find_rise_t_offset(self):
        lc = self.lc
        half_rise = find_rise_t(lc, 0.5, t_min=0, t_max=1)
        self.assertAlmostEqual(half_rise,0.5)
#
class TestOffsetPowerlawCurve(TestCase):
    def shortDescription(self):
        return None

    def test_linear_no_breaks(self):
        """
        Test the basic interface all works for a simple case.
        """
        lc = Powerlaw(init_amp=1, alpha_one=1, t_offset_min=1.0, t0=None)
        # Check negative handled by LightcurveBase
        self.assertEqual(lc(-1), 0.0)
        self.assertEqual(lc(1.01), 1.01)
        input_list = range(2,100)
        for posn in input_list:
            self.assertEqual(posn, lc(posn))

        input_array = np.arange(2, 100, np.pi)
        out_array = lc(input_array)
        self.assertTrue((input_array == out_array).all())
#
    def test_break(self):
        """
        Check that the break handling works as expected, for the simplest
        case where we maintain a linear slope.
        """
        lc = SingleBreakPowerlaw(init_amp=1,
                                 alpha_one=1.,
                                 break_one_t_offset=1.0,
                                 alpha_two=1.0,
                                 t_offset_min=1.0,
                                 t0=None)

        # Check negative handled by LightcurveBase
        self.assertEqual(lc(-1), 0.0)

        input_array = np.arange(2, 100, np.pi)
        out_array = lc(input_array)
        self.assertTrue((input_array == out_array).all())
