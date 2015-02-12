import scipy.optimize

import logging
logger = logging.getLogger(__name__)

def find_peak(curve, t_init=0.0):
    """
    Use scipy.optimize.fmin to locate a (possible local) maxima

    Returns:
        tuple: peak_t_offset, peak_flux
    """
    peak_t_offset = scipy.optimize.fmin(
        func=lambda t: -curve(t),
        x0=t_init,
        disp=False)[0]
    peak_flux = curve(peak_t_offset)
    if peak_flux == 0:
        raise ValueError("Numerical peak flux search returned 0 value, "
                         "suggests bad initialization.")
    return peak_t_offset, peak_flux

def find_rise_t_offset(curve, threshold, t_min,t_max):
    return scipy.optimize.bisect(f=lambda t: curve(t) - threshold,
                                 a=t_min,
                                 b=t_max)