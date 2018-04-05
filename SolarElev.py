#!/usr/bin/env python
"""
Computes solar irradiance and hence solar elevation angle for a year.
Updated to use AstroPy 1.0+, vectorized computation instead of PyEphem

If you'd like to incorporate a better spectral model like Lowtran or Hitran let me know.

Michael Hirsch
 Aug 2012 -- updated to Astropy Feb 2015
"""
from matplotlib.pyplot import show
#
import commsiteplan as csp
import commsiteplan.plots as cspp


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='plots solar elevation angle')
    p.add_argument('latlon',help='specify site lat lon [degrees] ',nargs=2,type=float)
    p.add_argument('-m','--minel',help='minimum usable solar elevation above horizon [deg]',type=float,default=10.)
    p.add_argument('-timestep', help='time step (hours)',type=int,default=2)
    p.add_argument('-year',help='year of prediction',type=int,default=2018)
    p = p.parse_args()

    Irr = csp.compsolar(p.latlon, p.minel, p.timestep, p.year)
# %% plots
    cspp.plotIrr(Irr)
    cspp.plotyear(Irr)
    cspp.plotenergy(Irr)

    show()
