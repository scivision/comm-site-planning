#!/usr/bin/env python
import numpy as np
from datetime import datetime
from dateutil.parser import parse
from matplotlib.pyplot import show
from argparse import ArgumentParser
#
import commsiteplan as csp
import commsiteplan.plots as cspp


def main():
    p = ArgumentParser(description='Simple model of solar irradiance at sea level.')
    p.add_argument('date', help='YYYY-mm-dd date', nargs='?')
    p.add_argument('-a', '--theta', help='angle(s) [deg] to compute sea level solar irradiance',
                   nargs='?', type=float, default=np.arange(0., 90+1, 1))
    p = p.parse_args()

    if p.date is not None:
        date = parse(p.date)
    else:
        date = datetime.today().date()

    Irr = csp.airmass(p.theta, date)

    if Irr.angle_deg.size > 1:
        cspp.plotam(Irr)
        show()
    else:
        print(f'Irradiance: {Irr["Irr"].item():0.1f} [W/m^2]  '
              f'Airmass relative to Zenith: {Irr["Am"].item():0.3f}')


if __name__ == '__main__':
    main()
