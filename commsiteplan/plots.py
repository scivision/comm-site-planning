from matplotlib.pyplot import figure


def plotyear(dates,hoursofday,sunel,site,obs,lbl,fmt):
    fg = figure(figsize=(12,7),dpi=100)
    ax = fg.gca()
    V = (-18,-12,-6,-3,0,10,20,30,40,50,60,70,80,90)
    CS = ax.contour(dates,hoursofday,sunel,V)
    ax.clabel(CS, inline=1, fontsize=10,fmt='%0.0f')#, manual=manual_locations)
    ax.set_ylabel('UTC')
    ax.set_title('Solar elevation angle (deg.)  {}: {:.1f},{:.1f}'.format(site,obs.latitude,obs.longitude))
    ax.grid(True)
#    fg.autofmt_xdate()
    ax.xaxis.set_major_locator(lbl)
    ax.xaxis.set_major_formatter(fmt)

def plotIrr(dates,hoursofday,sunel,site,obs,lbl,fmt):
    fg = figure(figsize=(12,7),dpi=100)
    ax = fg.gca()
    CS = ax.contour(dates,hoursofday,sunel)
    ax.clabel(CS, inline=1, fontsize=10,fmt='%0.0f')#, manual=manual_locations)
    ax.set_ylabel('UTC')
    ax.set_title('Sea level solar irradiance [W/m$^2$] at {}: {:.1f},{:.1f}'.format(site,obs.latitude,obs.longitude))
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

def plotenergy(Whr,dates,site,obs,lbl,fmt):
    ax = figure().gca()
    ax.plot(dates,Whr/1000)
    ax.set_xlabel('UTC')
    ax.set_ylabel('kWhr m$^{-2}$ day$^{-1}$')
    ax.set_title('Daily Solar Energy at {}: {:.1f}, {:.1f}'.format(site,obs.latitude,obs.longitude))
    ax.set_ylim(0,12)
    ax.xaxis.set_major_locator(lbl)
    ax.xaxis.set_major_formatter(fmt)


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

