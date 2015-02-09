import types
from collections import Iterable
import pandas as pd

def multifreq_daterange(start, *timedelta_freq_tuples):
    """
    Convenience wrapper around pandas.date_range, appends multiple
    date ranges with specified timedelta periods and frequency spacings.
    """
    rngs=[pd.Index([start])]
    for tdelta, freq in timedelta_freq_tuples:
        prev_end = rngs[-1][-1]
        rngs.append(pd.date_range(prev_end, prev_end + tdelta, freq=freq))
    epochs = sum(rngs)
    return epochs

def convert_to_timedeltas(epochs, epoch0):
    """
    Convert an epochs to timedeltas (in seconds), relative to epoch0.

    Args:
        epochs: Iterable containing datetimes, e.g. output from pandas.date_range.
        epoch0: Reference date-time.

    Returns:
        Series; timedeltas in seconds, indexed by epoch.
    """
    offsets = pd.Series(
        (pd.Series(epochs, index=epochs) - pd.Series(epoch0, index=epochs)
        ).astype('timedelta64[s]'),
        name='t_offset')
    return offsets

def listify(x):
    """Ensure x is iterable; if not then enclose it in a list and return it."""
    if isinstance(x, types.StringTypes):
        return [x]
    elif isinstance(x, Iterable):
        return x
    else:
        return [x]