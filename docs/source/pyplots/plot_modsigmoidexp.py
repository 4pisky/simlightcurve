from __future__ import absolute_import

import matplotlib.pyplot as plt
import numpy as np
import seaborn

from simlightcurve.curves import NormedModSigmoidExp as Hump

seaborn.set_context('poster')
seaborn.set_style("dark")


hr = 60*60
decay_tau=1.*24*hr
rise_tau=decay_tau*0.3
t1_offset = decay_tau
sn0 = Hump(rise_tau=rise_tau,decay_tau = decay_tau,
                peak_flux=1, b=0,
                t1_minus_t0=t1_offset)
sn1 = Hump(rise_tau=rise_tau,decay_tau = decay_tau,
                peak_flux=1, b=3e-10,
                t1_minus_t0=t1_offset)
tsteps = np.arange(sn0.t_offset_min*0.8, sn0.t_offset_max*0.8, 30)


fig, axes = plt.subplots(1,1)
fig.suptitle('SNe optical lightcurves', fontsize=36)
ax=axes
ax.axvline(0, ls='--')
ax.axvline(t1_offset, ls='--')
ax.set_xlabel('Time')
ax.set_ylabel('Flux')
ax.plot(tsteps, sn0.flux(tsteps), label='SN0')
ax.plot(tsteps, sn1.flux(tsteps), label='SN1')
ax.legend()

