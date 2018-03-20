 # -*- coding: utf-8 -*-
import numpy as np
from numpy import sin,cos
import xarray
from datetime import datetime
import astropy.units as u
from astropy.coordinates import get_sun, EarthLocation, AltAz
from astropy.time import Time
from dateutil.rrule import HOURLY,rrule
from matplotlib.dates import MonthLocator,DateFormatter

from .plots import plotIrr, plotyear, plotenergy

def compsolar(site,coord,year,minel,plotperhour,doplot=False):
    """
    site: arbitrary string
    coord: 2- or 3-tuple of WGS-84 coordinates in degrees optional altitude in meters
    year: CE calendar year
    minel: minimum solar elevation above horizon to consider usable for solar energy (degrees)
    plotperhour: smoother plot but longer time to compute
    doplot: boolean
    """
    if isinstance(year,datetime):
        year=year.year
#%%
    site = site.lower()
    if len(site)==0 and coord[0] is not None: # len(site) == 0 to be nicer than None for string proc.
        if len(coord)==2:
            coord.append(0.) #in case altitude not specified
        obs = EarthLocation(lat=coord[0]*u.deg, lon=coord[1]*u.deg, height=coord[2]*u.m)
    elif "sondrestrom" in site:
        obs = EarthLocation(lat=66.98*u.deg, lon=-50.94*u.deg, height=180*u.m)
    elif "pfisr" in site:
        obs = EarthLocation(lat=65.12*u.deg, lon=-147.49*u.deg, height=210*u.m)
    elif site == "bu":
        obs = EarthLocation(lat=42.4*u.deg, lon=-71.1*u.deg, height=5*u.m)
    elif "svalbard" in site:
        obs = EarthLocation(lat=78.23*u.deg, lon=15.4*u.deg, height=450*u.m)
    else:
        raise ValueError('you must specify a site or coordinates')

    plotperday = 24*plotperhour
    #don't fool around with Pandas or Numpy, since Numpy datetime64 doesn't work with Matplotlib
    times = list(rrule(HOURLY,
                       dtstart=datetime(year,1,1,0,0,0),
                       until=datetime(year,12,31,23,59,59)))

    dates = times[::plotperday]
    hoursofday = times[:plotperday]

    #yes, we need to feed times to observer and sun!
    sun = get_sun(Time(times)).transform_to(AltAz(obstime=times,location=obs))
    sunel = sun.alt.degree.reshape((plotperday,-1),order='F')

    Irr = airmass(sunel,times,minel)

    Irr = estenergy(Irr,hoursofday)

    if doplot:
        lbl=MonthLocator(range(1,13),bymonthday=15,interval=1)
        fmt=DateFormatter("%b")
        plotIrr(dates,hoursofday,Irr['Irr'],site,obs,lbl,fmt)
        plotyear(dates,hoursofday,sunel,site,obs,lbl,fmt)
        plotenergy(Irr['Whr'],dates,site,obs,lbl,fmt)

    return Irr,sunel


def estenergy(Irr,hoursofday):

    secs = [(h-hoursofday[0]).total_seconds()/3600 for h in hoursofday]
    Irr['Irr'].fillna(0.)

    Irr['Whr'] = np.trapz(Irr['Irr'],x=secs,axis=0)

    return Irr

#%%
def airmass(thetadeg,dtime,minelevation_deg=5.):
    """
    Michael Hirsch

    Those considering concentrated solar power systems need a more advanced analysis.
    Aerosols, clouds, dust, etc. are not considered.
    assumes observer at sea level
    input: theta [deg] true (not apparent) solar elevation angle above horizon

    minelevation_deg: arbitrary, since refraction is not considered, the results are highly suspect for
    sun near horizon. Also consider blockage by terrain/buildings.

    Note: use https://github.com/scivision/lowtran for far more precise modeling
    """
    doy = Time2doy(dtime)

    thd = np.atleast_1d(thetadeg)
    thd[(thd<minelevation_deg) | (thd>90)] = np.nan
    thr = np.radians(thd)
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
    I0 = 1367. * (1+0.034*cos(np.radians(360*doy/365.25))) # [W/m^2],

    Clearness = 1. #often there are clouds, etc. that make clearness much less than 1!

#%% again, very simplified. Use a better model for real work
    #oft cited from Meinel and Meinel 1976
    Irr =I0 * Clearness*0.7**Am.ravel()**0.678 #at sea level!

    if Irr.size == Am.size and Irr.ndim != Am.ndim:
        Irr = Irr.reshape(Am.shape)

    if Irr.ndim==1:
        A = xarray.Dataset(
                       {'Am':('angle_deg',Am),
                        'Irr':('angle_deg',Irr)},
                       coords={'angle_deg':thd},
                       attrs={'I0':I0.item()})
        A = A.dropna(how='all',dim='angle_deg')
    elif Irr.ndim==2:
        A = xarray.Dataset(
                        {'Am':(('hour','doy'),Am),
                         'Irr':(('hour','doy'),Irr)},
                         coords={'hour':range(24),
                                 'doy':range(365)})


    return A


def Time2doy(dtime:datetime) -> int:
    dtime = np.atleast_1d(dtime)

    doy = np.asarray([int(t.strftime('%j')) for t in dtime])

    return doy


def doy2monthday(doy):
    doy = np.atleast_1d(doy)
    """ day of year to month, day in datetime()"""
    mon = []; day = []
    for d in doy:
        dt = datetime.strptime(str(d),'%j')
        mon.append(dt.month)
        day.append(dt.day)

    return np.asarray(mon), np.asarray(day)
