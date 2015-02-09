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

unbroken_pl = curves.Powerlaw(init_amp=1,
                     init_alpha=-0.5)

offset_pl = curves.OffsetPowerlaw(init_amp=1,
                     init_alpha=-0.5,
                     flux_offset=0)

broken_pl = curves.Powerlaw(init_amp=.1,
                     init_alpha=-0.2,
                     breaks={0.5*decay_tau:-0.8})



tsteps = np.linspace(0, decay_tau*5, 500, dtype=np.float)


fig, axes = plt.subplots(1,1)
fig.suptitle('Powerlaws', fontsize=36)
ax=axes
# ax.axvline(0, ls='--')
# ax.axvline(t1_offset, ls='--')
ax.set_xlabel('Time')
ax.set_ylabel('Flux')
ax.plot(tsteps, unbroken_pl.flux(tsteps), label='Unbroken powerlaw')
ax.plot(tsteps, broken_pl.flux(tsteps), label='Broken powerlaw')
ax.plot(tsteps, offset_pl.flux(tsteps), label='Offset powerlaw', ls='--')
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_ylim(0.001,.1)
ax.legend()
ax.set_xlim(-10, max(tsteps))

