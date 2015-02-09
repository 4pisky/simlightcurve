import abc
import numpy as np
import scipy.optimize

class DictReprMixin(object):
    """Represent a class by printing its public attributes."""
    def __repr__(self):
        return (self.__class__.__name__ +
               repr({ k: self.__dict__[k] for k in self.__dict__
                        if not k.startswith('_')})
        )


class LightcurveBase(object):
    """
    Base class for representing lightcurves with a common interface.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _flux(self, t_offset):
        """
        Internal, 'unsafe' flux function (may return negative vals, NaNs etc).

        Implemented by subclasses.

        Calculates flux value at a given offset from the lightcurve's
        nominal 't0' timestamp.
        Note that the specific meaning of t0 is implementation-dependent.
        This function should return valid results (i.e. no NaNs or infs) between
        `self.offset_min` and `self.offset_max`.

        Args:
            t_offset (float or numpy.array): Offset in seconds from t0.
        """

    def flux(self, t_offset):
        """
        Wraps internal `_flux` function.

        This wrapper ensures that we:
         - return 0 outside valid t_offset range,
         - handle numpy array / scalar inputs and outputs,
         - and process everything as np.float type, which avoids many subtle
           bugs.

        """
        t_array=np.asarray(t_offset,dtype=np.float)
        if np.ndim(t_offset)==0:
            t_array=t_array.reshape((1,))
        valid_idx = (t_array > self.t_offset_min) & (t_array < self.t_offset_max)
        results = np.zeros_like(t_array)
        results[valid_idx] = self._flux(t_array[valid_idx])
        if np.ndim(t_offset)==0 and len(results)==1:
            return results[0]
        return results

    @abc.abstractproperty
    def t_offset_min(self):
        """
        Lower bound on t_offset beyond which we can sensibly assume flux==0.
        (property)
        """
        pass

    @abc.abstractproperty
    def t_offset_max(self):
        """
        Upper bound on t_offset beyond which we can sensibly assume flux==0.
        (property)
        """
        pass

    @abc.abstractproperty
    def peak_flux(self):
        """
        The (global) flux maximum (property)
        """

    @abc.abstractproperty
    def peak_t_offset(self):
        """
        t_offset of peak flux (property)
        """

    @abc.abstractmethod
    def find_rise_t_offset(self, threshold):
        """
        Find minimum t_offset for which flux is above threshold (may be None).

        Args:
            threshold (float): The flux value of interest.

        Returns:
            float: Seconds offset from t0 at which flux rise above
                threshold occurs.
        """

class PeakSolverMixin(object):
    """
    Implements some standard numerical routines for finding a lightcurve peak.

    Also implements a generic 'find_rise_t_offset' making use of the peak.
    """
    def __init__(self):
        super(PeakSolverMixin,self).__init__()
        #NB this value must be overridden per-subclass
        #It is included here for documentation purposes.
        self._peak_solver_x0 = None

        self._peak_flux = None
        self._peak_t_offset = None


    def _find_peak(self):
        if self._peak_solver_x0 is None:
            raise NotImplementedError(
                "Subclasses must override peak search starting point with a "
                "sensible value")
        self._peak_t_offset = scipy.optimize.fmin(
            func=lambda t: -self.flux(t),
            x0=self._peak_solver_x0,
            disp=False)[0]
        self._peak_flux = self.flux(self._peak_t_offset)
        if self._peak_flux == 0:
            raise ValueError("Numerical peak flux search returned 0 value, "
                             "suggests bad initialization.")

    @property
    def peak_flux(self):
        if self._peak_flux is None:
            self._find_peak()
        return self._peak_flux

    @property
    def peak_t_offset(self):
        if self._peak_t_offset is None:
            self._find_peak()
        return self._peak_t_offset

class RiseTimeBisectMixin(object):
    def find_rise_t_offset(self, threshold):
        if threshold > self.peak_flux:
            return None
        return scipy.optimize.bisect(f=lambda t: self.flux(t) - threshold,
                                     a=self.t_offset_min,
                                     b=self.peak_t_offset)