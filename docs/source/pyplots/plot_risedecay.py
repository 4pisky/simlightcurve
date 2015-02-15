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

fred = curves.LinearExp(
    rise_time=rise_tau*1.5,
    decay_tau=decay_tau,
    amplitude=1.0)

gred = curves.GaussExp(
            rise_tau=rise_tau,
            decay_tau=decay_tau,
            amplitude=1.0)

grpld = curves.GaussPowerlaw(
    amplitude = 1.0,
    rise_tau=rise_tau,
    decay_alpha=-1.5,
    decay_offset=decay_tau,
    # breaks={0.1*decay_tau:-.1,
    #         0.5*decay_tau:-.5}
)

tsteps = np.arange(-rise_tau*3, decay_tau*5, 30)


fig, axes = plt.subplots(1,1)
fig.suptitle('Various rise and decay models', fontsize=36)
ax=axes
# ax.axvline(0, ls='--')
# ax.axvline(t1_offset, ls='--')
ax.set_xlabel('Time')
ax.set_ylabel('Flux')
ax.plot(tsteps, fred(tsteps), label='FRED', ls='--')
ax.plot(tsteps, gred(tsteps), label='GRED', ls='--')
ax.plot(tsteps, grpld(tsteps), label='GRPLD')
# ax.set_xscale('log')
# ax.set_yscale('log')
ax.set_ylim(1e-5,1.001)
ax.legend()

