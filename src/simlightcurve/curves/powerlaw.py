from __future__ import absolute_import, division
import numpy as np
from astropy.modeling import FittableModel, Parameter



def _calculate_powerlaw_break_amplitudes(init_amp, alpha_one,
                                         t_offset_min,
                                         breaks=None):
    """
    Calculate the per-stage amplitudes for each leg of a broken powerlaw curve.

    Args:
        init_amp (float): Initial Amplitude
        init_alpha (float): Initial Power-law index
        breaks (dict): Any power-law breaks.
            Dict maps 't_offset of break' -> 'index after break'
    """
    if init_amp == 0:
        raise ValueError("init_amp=0 always results in a flat lightcurve."
                         "Use the Null lightcurve if that's intended.")

    # Construct our fence-posts
    bounds = [t_offset_min]
    alphas = [float(alpha_one)]
    if breaks is not None:
        for break_posn in sorted(breaks.keys()):
            bounds.append(float(break_posn))
            alphas.append(float(breaks[break_posn]))
    bounds.append(float('inf'))

    # Calculate new amplitude to match new and old power-law values
    # at each break:
    amps = [init_amp]
    for idx in range(1, len(alphas)):
        value_at_break = (amps[-1]
                          * np.power(bounds[idx],
                                     alphas[idx - 1]))
        amps.append(
            value_at_break / np.power(bounds[idx],
                                      alphas[idx])
        )
    return bounds, alphas, amps


def _evaluate_broken_powerlaw(t_offset, bounds, alphas, amps):
    result = np.zeros_like(t_offset)
    for idx in range(0, (len(bounds) - 1)):
        lower = bounds[idx]
        upper = bounds[idx + 1]
        t_range = np.logical_and(t_offset >= lower , t_offset < upper)
        result[t_range] = (
            amps[idx] * np.power(t_offset[t_range], alphas[idx])
        )
    return result


class Powerlaw(FittableModel):
    """
    Represents a simple power-law curve

    The curve is defined as

        amplitude * (t_offset)**alpha

    Be wary of using an init_alpha<0, since this results in an asymptote at
    t=0.

    NB  The curve will always begin at the origin, because maths.
    (Cannot raise a negative number to a fractional power unless you
    deal with complex numbers. Also 0.**Y == 0. )
    """
    inputs=('t',)
    outputs=('flux',)

    init_amp = Parameter()
    alpha_one = Parameter()
    t_offset_min = Parameter(default=0.)
    t0 = Parameter(default=0.)

    @staticmethod
    def evaluate(t,
             init_amp,
             alpha_one,
             t_offset_min,
             t0
    ):
        if np.ndim(t)==0:
            t=np.asarray(t,dtype=np.float).reshape((1,))
        t_offset = t-t0
        result = np.zeros_like(t_offset)
        t_valid = t_offset >= t_offset_min
        result[t_valid] = ( init_amp* np.power(t_offset[t_valid], alpha_one))
        return result



class SingleBreakPowerlaw(FittableModel):
    """
    Represents an power-law curve with a single index-break

    The curve is defined as

        init_amplitude * (t_offset)**alpha_one

    until the location of the first index-break, then
        matched_amplitude * (t_offset)**alpha_two

    where matched_amplitude is calculated to ensure the curves meet at the
    power-break location.

    We wary of using an init_alpha<0, since this results in an asymptote at
    t=0.

    NB  The curve will always begin at the origin, because maths.
    (Cannot raise a negative number to a fractional power unless you
    deal with complex numbers. Also 0.**Y == 0. )
    """

    inputs = ('t',)
    outputs = ('flux',)

    init_amp = Parameter()
    alpha_one = Parameter()
    break_one_t_offset = Parameter()
    alpha_two = Parameter()
    t_offset_min = Parameter(default=0.)
    t0 = Parameter(default=0.)

    @staticmethod
    def evaluate(t,
             init_amp,
             alpha_one,
             break_one_t_offset,
             alpha_two,
             t_offset_min,
             t0
    ):
        if np.ndim(t) == 0:
            t = np.asarray(t, dtype=np.float).reshape((1,))
        t_offset = t - t0
        bounds, alphas, amps = _calculate_powerlaw_break_amplitudes(
            init_amp, alpha_one, t_offset_min,
            breaks={break_one_t_offset[0]: alpha_two[0]})
        return _evaluate_broken_powerlaw(t_offset, bounds, alphas, amps)
