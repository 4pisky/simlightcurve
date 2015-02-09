from __future__ import absolute_import, division
import numpy as np
from simlightcurve.lightcurve import (DictReprMixin, LightcurveBase,
                                      PeakSolverMixin, RiseTimeBisectMixin)


class Powerlaw(PeakSolverMixin,RiseTimeBisectMixin,LightcurveBase,
               DictReprMixin):
    def __init__(self, init_amp, init_alpha, breaks=None):
        """
        Represents a power-law curve, with optional power-breaks.

        The curve is defined as

            init_amp * (t_offset)**init_alpha

        in the no-breaks case. NB:

            base = t

        We wary of using an init_alpha<0, since this results in an asymptote at
        t=0.


        Args:
            init_amp (float): Initial Amplitude
            init_alpha (float): Initial Power-law index
            breaks (dict): Any power-law breaks.
                Dict maps 't_offset of break' -> 'index after break'

        NB  The curve will always begin at the origin, because maths.
        (Cannot raise a negative number to a fractional power unless you
        get all complex. Also 0.**Y == 0. )
        """
        super(Powerlaw, self).__init__()

        self._peak_solver_x0 = 0.


        if init_amp == 0:
            raise ValueError("init_amp=0 always results in a flat lightcurve."
                             "Use the Null lightcurve if that's intended.")

        # Construct our fence-posts
        self.bounds = [0.]
        self.alphas = [float(init_alpha)]
        if breaks is not None:
            for break_posn in sorted(breaks.keys()):
                self.bounds.append(float(break_posn))
                self.alphas.append(float(breaks[break_posn]))
        self.bounds.append(float('inf'))

        # Calculate new amplitude to match new and old power-law values
        # at each break:
        self.amps = [init_amp]
        for idx in range(1, len(self.alphas)):
            value_at_break = (self.amps[-1]
                              * np.power(self.bounds[idx],
                                         self.alphas[idx - 1]))
            self.amps.append(
                value_at_break / np.power(self.bounds[idx],
                                          self.alphas[idx])
            )

    def _flux(self, t_offset):
        result = np.zeros_like(t_offset)
        for idx in range(0, (len(self.bounds) - 1)):
            lower = self.bounds[idx]
            upper = self.bounds[idx + 1]
            t_range = (t_offset > lower) & (t_offset <= upper)
            result[t_range] = (
                self.amps[idx] * np.power(t_offset[t_range], self.alphas[idx])
            )
        return result

    @property
    def t_offset_min(self):
        return 0.

    @property
    def t_offset_max(self):
        #We can do better, if necessary... but this is fine for now.
        return float('inf')



class OffsetPowerlaw(PeakSolverMixin,RiseTimeBisectMixin,LightcurveBase,
                     DictReprMixin):
    def __init__(self, init_amp, init_alpha, flux_offset,
                 breaks=None):
        """
        Represents a shifted-by-one power-law curve, with optional power-breaks.

        This curve is defined as

            init_amp * (t_offset + 1)**init_alpha + flux_offset

        in the no-breaks case. NB:
            base = t+1

        We then add a flux_offset to raise or lower the intercept, which becomes

            y(0) = init_amp + flux_offset

        This makes it much easier to reason about the lightcurve's
        characteristics for small t (no asymptotic behaviour),
        although the slope will be different to a zero-origin powerlaw at
        small t. As a consequence, any breaks in the powerlaw at small t will
        result in significantly different amplitudes later on (compared to the
        regular powerlaw), due to the chain-effect of the amplitude matching at
        break-points.

        Args:
            init_amp (float): Initial Amplitude
            init_alpha (float): Initial Power-law index
            flux_offset(float): Constant added to resulting flux values.
            break_alpha_tuples (dict): Any power-law breaks.
                Dict maps 't_offset of break' -> 'index after break'

        NB  The curve will always begin at the origin, because maths.
        (Cannot raise a negative number to a fractional power unless you
        get all complex. Also 0.**Y == 0. )
        """
        super(OffsetPowerlaw, self).__init__()

        offset_breaks=None
        if breaks is not None:
            offset_breaks = { k + 1.0: v for k,v in breaks.iteritems()}

        self._wrapped_powerlaw = Powerlaw(init_amp=init_amp,
                                          init_alpha=init_alpha,
                                          breaks=offset_breaks)
        self._peak_solver_x0 = 0.
        self._flux_offset = flux_offset

    def _flux(self, t_offset):
        return self._wrapped_powerlaw._flux(t_offset+1)+self._flux_offset

    @property
    def t_offset_min(self):
        return 0.

    @property
    def t_offset_max(self):
        #We can do better, if necessary... but this is fine for now.
        return float('inf')
