from __future__ import absolute_import, division
import numpy as np
import scipy as sp
from scipy.optimize import fsolve
from astropy.modeling import FittableModel, Parameter


def tau_0_solve(x, energy_index):
    return np.exp(x) - (energy_index + 4.) / 5. - 1.


class vdl(FittableModel):
    inputs = ('t',)
    outputs = ('flux',)

    energy_index = Parameter()
    maximum_flux = Parameter()
    maximum_time = Parameter()

    @staticmethod
    def evaluate(t, energy_index, maximum_flux, maximum_time):
        vals = np.zeros_like(t, dtype=np.float)
        index = t >= 0.

        # parameters that are derived from inputs and physics parameters
        distance = 3.09e19  # place holder distance of 1 kiloparsec
        initial_tau_0_guess = 10.
        tau_m = fsolve(tau_0_solve, initial_tau_0_guess, energy_index)
        size_at_peak_flux = ((maximum_flux * distance * distance / np.pi) * (1. / (1. - np.exp(-tau_m)))) ** 0.5
        expansion_speed = size_at_peak_flux / maximum_time

        # assume that the cloud expands linearly
        relative_size = 1. + (expansion_speed / size_at_peak_flux) * (t - maximum_time)

        numerator = 1. - np.exp(-tau_m * relative_size ** (-2. * energy_index - 3.))
        denominator = 1. - np.exp(-tau_m)
        vals[index] = (relative_size ** 3.) * numerator / denominator

        return  maximum_flux * vals
