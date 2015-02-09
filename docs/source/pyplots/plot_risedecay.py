from __future__ import absolute_import

import matplotlib.pyplot as plt
import numpy as np
import seaborn

from simlightcurve import curves

seaborn.set_context('poster')
seaborn.set_style("dark")


hr = 60*60
decay_tau=1.*24*hr
rise_tau=decay_tau*0.3
t1_offset = decay_tau
fred = curves.LinearExp(rise_time=rise_tau*1.5,
            decay_tau=decay_tau,
            peak_flux=1.0)

gred = curves.GaussExp(rise_tau=rise_tau,
            decay_tau=decay_tau,
            peak_flux=1.0)

grpld = curves.GaussPowerlaw(rise_tau=rise_tau,
            init_alpha=-.005,
            peak_flux=1.0,
            breaks={0.1*decay_tau:-.1,
                    0.5*decay_tau:-.5}
)

tsteps = np.arange(gred.t_offset_min, decay_tau*5, 30)


fig, axes = plt.subplots(1,1)
fig.suptitle('Various rise and decay models', fontsize=36)
ax=axes
# ax.axvline(0, ls='--')
# ax.axvline(t1_offset, ls='--')
ax.set_xlabel('Time')
ax.set_ylabel('Flux')
ax.plot(tsteps, fred.flux(tsteps), label='FRED', ls='--')
ax.plot(tsteps, gred.flux(tsteps), label='GRED', ls='--')
ax.plot(tsteps, grpld.flux(tsteps), label='GRPLD')
# ax.set_xscale('log')
# ax.set_yscale('log')
ax.set_ylim(1e-5,1.001)
ax.legend()

