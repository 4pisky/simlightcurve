from __future__ import absolute_import

import matplotlib.pyplot as plt
import numpy as np
import seaborn

from simlightcurve.curves import Minishell

seaborn.set_context('poster')
seaborn.set_style("dark")
seaborn.set_palette('husl')


hr=3600.0
day = 24*hr
timespan = 1000*day
tsteps = np.linspace(day,timespan,day)
afterglow = Minishell(k1=2.5e2, k2=1.38e2, k3=1.47e5,
                      beta=-1.5, delta1=-2.56, delta2=-2.69)

fig, axes = plt.subplots(1,1)
fig.suptitle('SNe radio lightcurve', fontsize=36)
lc = afterglow.flux(tsteps)
axes.plot(tsteps, lc)
axes.set_xlabel('Time')
axes.set_ylabel('Flux')
axes.set_xscale('log')
axes.set_yscale('log')
axes.set_ylim(0.001,np.max(lc)+0.2)
axes.set_xlim(2*day,timespan)




