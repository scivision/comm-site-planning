#!/usr/bin/env python
"""
Computes solar irradiance and hence solar elevation angle for a year.
Updated to use AstroPy 1.0+, vectorized computation instead of PyEphem

If you'd like to incorporate a better spectral model like Lowtran or Hitran let me know.

Michael Hirsch
 Aug 2012 -- updated to Astropy Feb 2015
"""
from commsiteplan import compsolar
from matplotlib.pyplot import show
try:
    import seaborn as sns
    sns.color_palette(sns.color_palette("cubehelix"))
    sns.set(context='poster', style='whitegrid')
    sns.set(rc={'image.cmap': 'cubehelix_r'}) #for contour
except ImportError:
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='plots solar elevation angle')

    pg = p.add_mutually_exclusive_group(required=True)
    pg.add_argument('-s','--site',help='use a prestored site [sondrestrom, pfisr, bu, svalbard]', default='')
    pg.add_argument('-c','--coord',help='specify site lat lon [degrees] ',nargs=2,type=float)

    p.add_argument('-m','--minel',help='minimum usable solar elevation above horizon [deg]',type=float,default=10.)
    p.add_argument('--pph', help='plot steps per hour (default 1)',type=int,default=1)
    p.add_argument('--noplot',help='disable plotting',action='store_false')
    p = p.parse_args()

    doplot = p.noplot

    Irr, sunel = compsolar(p.site, p.coord, 2013, p.minel, p.pph, doplot)

    show()
