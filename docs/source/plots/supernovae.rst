.. _plots_sne:

Supernovae
============


Optical
-------

Make use of the quadratically-modulated sigmoidal rise / exponential decay, cf
Karpenka 2012 and references therein:

Class: :py:class:`~simlightcurve.curves.modsigmoid.NormedModSigmoidExp`

.. plot:: pyplots/plot_modsigmoidexp.py


Radio
-----

Make use of the 'minishell' model, a product of factors including exponential
decay and power law, following VAST memo #3, Ryder 2010
( http://www.physics.usyd.edu.au/sifa/vast/uploads/Main/vast_memo3.pdf )

Class: :py:class:`~simlightcurve.curves.minishell.Minishell`

.. plot:: pyplots/plot_minishell.py
