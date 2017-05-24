#!/usr/bin/env python
import numpy as np
from datetime import datetime
from matplotlib.pyplot import show
#
from commsiteplan import airmass
from commsiteplan.plots import plotam

if __name__ =='__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='trivial model of solar irradiance at sea level. Use Lowtran or Hitran for more detailed modeling')
    p.add_argument('-a','--theta',help='angle(s) [deg] to compute sea level solar irradiance',nargs='?',type=float,default=np.arange(0.,90+1,1))
    p.add_argument('-d','--dtime',help='YYYY-mm-dd date',nargs='?',default='2015-03-06',type=str)
    p = p.parse_args()

    dtime = datetime.strptime(p.dtime,'%Y-%m-%d')

    Irr,M,I0 = airmass(p.theta,dtime)
    if Irr.size > 1:
        plotam(Irr,M,I0,p.theta)
        show()
    else:
        print('Irr: {:0.1f} [W/m^2]   Airmass relative to Zenith: {:0.3f}'.format(Irr,M))