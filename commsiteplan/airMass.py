#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Michael Hirsch

This function is for thinking about a solar power system.
Those considering concentrated solar power systems need a more advanced analysis.
Aerosols, clouds, dust, etc. are not considered.
assumes observer at sea level
input: theta [deg] true (not apparent) solar elevation angle above horizon

minelevation_deg: arbitrary, since refraction is not considered, the results are highly suspect for
sun near horizon. Also consider blockage by terrain/buildings.

Note: use https://github.com/scienceopen/lowtran for far more precise modeling
"""
from __future__ import division
from numpy import sin,radians,arange,copy,nan,cos,atleast_1d,asarray,empty_like
from datetime import datetime

def airmass(thetadeg,dtime,minelevation_deg=5.):
    doy = Time2doy(dtime)

    thd = copy(thetadeg) #copy() so we don't corrupt the calling function!
    thd[(thd<minelevation_deg) | (thd>90)] = nan
    thr = radians(thd)
#%% Air mass model (very simple model)
    """
    Kasten, F., and A. T. Young. 1989. Revised optical air mass tables and approximation formula.
    Applied Optics 28:4735–4738. doi: 10.1364/AO.28.004735
    """
    #Am = 1/(sin(thr) + 0.50572*(6.07995+thetadeg)**-1.6364) #air mass factor
    """
    Young, A. T. 1994. Air mass and refraction. Applied Optics. 33:1108–1110. doi: 10.1364/AO.33.001108.
    Eqn (5) from paper, Eqn(5.23) in Paulescu et al 2013
    For sea-level, neglects aerosols, ozone, etc.
    Also neglects the effects of refraction--theta is "true" elevation angle w/o refraction.
    """
    Am = ((1.002432*sin(thr)**2 + 0.148386*sin(thr) + 0.0096467) /
          (sin(thr)**3 + 0.149864*sin(thr)**2 + 0.0102963*sin(thr) + 0.000303978))

#%%
    """
    AM0 ~ 1367 W/m^2 extraterrestrial solar flux at 1AU
    M. Paulescu, E. Paulescu, P. Gravila, V. Badescu 2013
    978-1-4471-4649-0
    "Weather Modeling and Forecasting of PV Systems Operation"
    http://link.springer.com/book/10.1007/978-1-4471-4649-0

    L. Wong, W. Chow "Solar radiation model" App. Energy 69 2001 191-224

    D. Goswami, F. Kreith, J. Krieder "Principles of Solar Engineering," 2nd Ed. 2000
    """
    I0 = 1367. * (1+0.034*cos(radians(360*doy/365.25))) # [W/m^2],

    Clearness = 1. #often there are clouds, etc. that make clearness much less than 1!

#%% again, very simplified. Use a better model for real work
    #oft cited from Meinel and Meinel 1976
    Irr =I0 * Clearness*0.7**Am.ravel()**0.678 #at sea level!

    if Irr.size == Am.size and Irr.ndim != Am.ndim:
        Irr = Irr.reshape(Am.shape)

    return Irr, Am,I0

def Time2doy(dtime):
    dtime = atleast_1d(dtime)
    try:
        doy = empty_like(dtime,dtype=int)
        for i,t in enumerate(dtime):
            if isinstance(t,datetime):
                doy[i] = int(t.strftime('%j'))
            else: #assuming astropy.Time
                doy[i] = int(t.datetime.strftime('%j'))
    except (TypeError,AttributeError):
        pass #already doy (we hope)
    return doy

def doy2monthday(doy):
    doy = atleast_1d(doy)
    """ day of year to month, day in datetime()"""
    mon = []; day = []
    for d in doy:
        dt = datetime.strptime(str(d),'%j')
        mon.append(dt.month)
        day.append(dt.day)
    return asarray(mon),asarray(day)

def plotam(Irr,M,I0,theta):
    ax=figure().gca()
    ax.plot(theta,Irr.T)
    ax.set_title('Solar Irradiance at sea level vs. Solar Elevation Angle',fontsize='x-large')
    ax.set_xlabel('Solar Elevation Angle  [deg.]',fontsize='large')
    ax.set_ylabel('Solar Irradiance at sea level [W m$^2$]',fontsize='large')
    #ax.legend(loc='best')
    ax.grid(True)

    ax=figure().gca()
    ax.plot(theta,M)
    ax.set_xlabel('Solar Elevation Angle  [deg.]',fontsize='large')
    ax.set_ylabel('Air Mass relative to zenith',fontsize='large')
    ax.set_title('Relative Air Mass vs. elevation angle',fontsize='large')
    ax.grid(True)


if __name__ =='__main__':
    from matplotlib.pyplot import figure,show
    from argparse import ArgumentParser
    p = ArgumentParser(description='trivial model of solar irradiance at sea level. Use Lowtran or Hitran for more detailed modeling')
    p.add_argument('-a','--theta',help='angle(s) [deg] to compute sea level solar irradiance',nargs='?',type=float,default=arange(0.,90+1,1))
    p.add_argument('-d','--dtime',help='YYYY-mm-dd date',nargs='?',default='2015-03-06',type=str)
    p = p.parse_args()

    dtime = datetime.strptime(p.dtime,'%Y-%m-%d')

    Irr,M,I0 = airmass(p.theta,dtime)
    if Irr.size > 1:
        plotam(Irr,M,I0,p.theta)
        show()
    else:
        print('Irr: {:0.1f} [W/m^2]   Airmass relative to Zenith: {:0.3f}'.format(Irr,M))
