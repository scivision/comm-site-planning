import xarray
from matplotlib.pyplot import figure
from matplotlib.dates import MonthLocator,DateFormatter

lbl=MonthLocator(range(1,13),bymonthday=15,interval=1)
fmt=DateFormatter("%b")

def plotyear(Irr:xarray.Dataset):
    if Irr['sunel'].dropna(dim='hour',how='all').shape[0] < 4:
        return

    fg = figure(figsize=(12,7),dpi=100)
    ax = fg.gca()
    V = (-18,-12,-6,-3,0,10,20,30,40,50,60,70,80,90)
    CS = ax.contour(Irr.date.values, Irr.hour.values, Irr['sunel'].values,V)
    ax.clabel(CS, inline=1, fontsize=10,fmt='%0.0f')#, manual=manual_locations)
    ax.set_ylabel('UTC')
    ax.set_title('Solar elevation angle (deg.)  {:.1f},{:.1f}'.format(Irr.lat, Irr.lon))
    ax.grid(True)
#    fg.autofmt_xdate()
    ax.xaxis.set_major_locator(lbl)
    ax.xaxis.set_major_formatter(fmt)

def plotIrr(Irr:xarray.Dataset):
    fg = figure(figsize=(12,7),dpi=100)
    ax = fg.gca()
    CS = ax.contour(Irr.date.values, Irr.hour.values, Irr['Irr'])
    ax.clabel(CS, inline=1, fontsize=10,fmt='%0.0f')#, manual=manual_locations)
    ax.set_ylabel('UTC')
    ax.set_title('Sea level solar irradiance [W/m$^2$] {:.1f},{:.1f}'.format(Irr.lat, Irr.lon))
    ax.grid(True)
#    fg.autofmt_xdate()
    ax.xaxis.set_major_locator(lbl)
    ax.xaxis.set_major_formatter(fmt)

def plotday(t,sunalt,site):
    ax = figure().gca()
    ax.plot(t,sunalt)
    ax.set_ylabel('Solar elevation [deg.]')
    ax.set_xlabel('UTC')
    ax.grid(True)
    ax.set_title('{} {}'.format(site,t[0].strftime('%Y-%m-%d')))

def plotenergy(Irr):
    ax = figure().gca()
    ax.plot(Irr.date, Irr['Whr']/1000)
    ax.set_xlabel('UTC')
    ax.set_ylabel('kWhr m$^{-2}$ day$^{-1}$')
    ax.set_title('Daily Solar Energy  {:.1f}, {:.1f}'.format(Irr.lat, Irr.lon))
    ax.set_ylim(0,12)
    ax.xaxis.set_major_locator(lbl)
    ax.xaxis.set_major_formatter(fmt)


def plotam(Irr):
    ax=figure().gca()
    ax.plot(Irr.angle_deg, Irr['Irr'])
    ax.set_title('Solar Irradiance at sea level vs. Solar Elevation Angle',fontsize='x-large')
    ax.set_xlabel('Solar Elevation Angle  [deg.]',fontsize='large')
    ax.set_ylabel('Solar Irradiance at sea level [W m$^2$]',fontsize='large')
    #ax.legend(loc='best')
    ax.grid(True)

    ax=figure().gca()
    ax.plot(Irr.angle_deg, Irr['Am'])
    ax.set_xlabel('Solar Elevation Angle  [deg.]',fontsize='large')
    ax.set_ylabel('Air Mass relative to zenith',fontsize='large')
    ax.set_title('Relative Air Mass vs. elevation angle',fontsize='large')
    ax.grid(True)

