from __future__ import absolute_import
import datetime
from datetime import timedelta
from unittest import TestCase
import math
import scipy.stats
import simlightcurve.curves as simlc


class TestLinearRiseExpDecay(TestCase):
    def shortDescription(self):
        return None

    def setUp(self):
        self.rise_time = 60 * 60
        self.decay_tau = 10 * 60 * 60
        self.amplitude = 1
        self.lc = simlc.LinearExp(
            rise_time=self.rise_time,
            decay_tau=self.decay_tau,
            amplitude=self.amplitude)

    def test_rising_flux(self):
        # Check out of bounds handled correctly
        self.assertEqual(self.lc(-1.01 * self.rise_time), 0.0)
        #Simple linear rise
        self.assertEqual(self.lc(-0.5 * self.rise_time),
                         self.amplitude / 2.0)


    def test_decay_flux(self):
        self.assertEqual(self.lc(self.decay_tau),
                         self.amplitude / math.exp(1.0))
        self.assertAlmostEqual(self.lc(1.5 * self.decay_tau),
                               self.amplitude / math.exp(1.5))

class TestGaussRiseExpDecay(TestCase):
    def shortDescription(self):
        return None

    def setUp(self):
        self.rise_tau= 60 * 60
        self.decay_tau = 10 * 60 * 60
        self.amplitude = 1.0
        self.lc = simlc.GaussExp(
            rise_tau=self.rise_tau,
            decay_tau=self.decay_tau,
            amplitude=self.amplitude)

    def test_amplitude(self):
        self.assertEqual(self.lc([0]), self.amplitude)

    def test_rising_flux(self):
        #Simple linear rise
        def known_gauss(x):
            return scipy.stats.norm().pdf(x)*math.sqrt(2*math.pi)
        self.assertEqual(self.lc(-0.5 * self.rise_tau),
                         known_gauss(-0.5))

    #
    def test_decay_flux(self):
        self.assertEqual(self.lc([self.decay_tau]),
                         self.amplitude / math.exp(1.0))
        self.assertAlmostEqual(self.lc([1.5 * self.decay_tau]),
                               self.amplitude / math.exp(1.5))