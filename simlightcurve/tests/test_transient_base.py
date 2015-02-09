from __future__ import absolute_import
from unittest import TestCase
from datetime import date, time, datetime, timedelta
import pandas as pd

from simlightcurve.transient import TransientBase
from simlightcurve.curves import Null, NegativeQuadratic


class ExampleTransient(TransientBase):
    def __init__(self,epoch0):
        super(ExampleTransient, self).__init__(epoch0=epoch0)
        self._add_lightcurve('optical',0,NegativeQuadratic(peak=10.0))
        self._add_lightcurve('radio', 4, NegativeQuadratic(peak=5.0))

class TestFluxAt(TestCase):
    """
    Test the wrapper function that pulls timestamped flux for constituent
    lightcurves.
    """
    def setUp(self):
        self.epoch0 = datetime.combine(date(2015,1,1),time())
        self.transient = ExampleTransient(self.epoch0)

    def test_single_epoch(self):
        e0_flux = self.transient.flux_at(self.epoch0)
        self.assertEqual(len(e0_flux),1)
        #NB pandas flexi-indexing, can index by key ("loc"):
        self.assertEqual(e0_flux.optical.loc[self.epoch0], 10)
        #Or by position ("iloc", short for integer location):
        self.assertEqual(e0_flux.radio.iloc[0], 0)

    def test_multi_epoch(self):
        epochs = pd.date_range(start=self.epoch0-timedelta(seconds=5),
                               end=self.epoch0+timedelta(seconds=10),
                               freq='S')
        fluxes = self.transient.flux_at(epochs)
        # print fluxes
        self.assertEqual(fluxes.optical.loc[self.epoch0],10)
        self.assertEqual(fluxes.radio.loc[self.epoch0],0)

        t_plus_3 = self.epoch0+timedelta(seconds=3)
        self.assertEqual(fluxes.optical.loc[t_plus_3],10-3*3)
        self.assertEqual(fluxes.radio.loc[t_plus_3],5-1)

        t_plus_4 = self.epoch0+timedelta(seconds=4)
        self.assertEqual(fluxes.optical.loc[t_plus_4],0)
        self.assertEqual(fluxes.radio.loc[t_plus_4],5)

class TestRiseTime(TestCase):
    """
    Test wrapper which converts a flux-threshold rise time_offset to a
    timestamp.
    """
    def setUp(self):
        self.epoch0 = datetime.combine(date(2015,1,1),time())
        self.transient = ExampleTransient(self.epoch0)

    def test_find_rise_time(self):
        opt_rise_time = self.transient.find_rise_time('optical', 9)
        self.assertEqual(self.epoch0 - timedelta(seconds=1), opt_rise_time)
        #Must account for lag in radio:
        rad_rise_time = self.transient.find_rise_time('radio', 4)
        self.assertEqual(self.epoch0 + timedelta(seconds=3), rad_rise_time)


