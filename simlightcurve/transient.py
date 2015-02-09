from __future__ import absolute_import
from pandas import Series, DataFrame
from datetime import timedelta
from simlightcurve.utils import convert_to_timedeltas, listify
from simlightcurve.lightcurve import LightcurveBase


class TransientBase(object):
    """
    A suggested starting point for defining multi-wavelength transient models.
    """
    def __init__(self, epoch0):
        """
        Assigns nominal 'epoch0' to reference per-band lightcurves against.

        ``self.lightcurves`` is a Dataframe, one column per waveband.
        """
        self.epoch0 = epoch0
        self.lightcurves = DataFrame(index=['curve','lag_seconds'])

    def class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return "{}({})".format(self.class_name(), self.epoch0)

    def __repr__(self):
        return "{}({})".format(self.class_name(), repr(self.epoch0))

    def _add_lightcurve(self, waveband, lag, lightcurve):
        """
        Args:
            waveband (str): Name of the waveband represented
            lag (float or timedelta): Time-delay between self.epoch0 and the
                t0 for this lightcurve. Can be passed as a float representing
                seconds, or a datetime.timedelta object.
            lightcurve: The LightcurveBase derived class defining the flux.
        """
        if hasattr(lag, "total_seconds"):
            lag = lag.total_seconds()
        self.lightcurves[waveband] = Series([lightcurve,lag],
                                            index=self.lightcurves.index)

    def flux_at(self, epochs, waveband=None):
        if waveband is None:
            waveband=self.lightcurves.columns
        else:
            waveband=listify(waveband)
        epochs=listify(epochs)
        t0_offsets = convert_to_timedeltas(epochs, self.epoch0)
        results = DataFrame(index=epochs)
        results.index.name = 'epoch'
        for wb in waveband:
            waveband_t_inputs = t0_offsets - self.lightcurves[wb].lag_seconds
            waveband_fluxes = self.lightcurves[wb].curve.flux(waveband_t_inputs)
            results[wb] = Series(index=epochs,
                                 data=waveband_fluxes)
        return results

    def find_rise_time(self, waveband, flux_threshold):
        band = self.lightcurves[waveband]
        assert isinstance(band.curve, LightcurveBase)
        t_off_sec = band.curve.find_rise_t_offset(flux_threshold)
        t_off = timedelta(
            seconds=band.lag_seconds+t_off_sec)
        return self.epoch0+t_off