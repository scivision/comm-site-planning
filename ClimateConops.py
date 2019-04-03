#!/usr/bin/env python
"""
Michael Hirsch
Thanks to Amber Baurley and Sam Chen for climate research
 crude thermal budget for outdoor enclosure
 we consider arbitrarily two worst case dates:
 Dec 21 worst-case heating need -- 10th percentile
 Sept 1 worst-case cooling need

My example case (your parameters will be different!)

./ClimateConops.py 250 5 0.18 0.7
"""
from argparse import ArgumentParser
from numpy import sin, radians
from typing import Dict
#
# Qequip = { 'rest': 125, 'record': 175, 'compress': 250, 'off':5 } #[W]
#
"""
user input: plug in the area of your enclosure faces in Areas
"""
# [m^2] area of the panel
Areas = [{'side': 0.45, 'end': 0.35, 'top': 0.45, 'model': 'Zarges'},
         {'side': 0.51, 'end': 0.5, 'top': 0.41, 'model': 'OD-30DXC'}]


def main():
    p = ArgumentParser(description='very simple steady state thermodynamic enclosure analysis')
    p.add_argument('Qonoff', help='Power consumption of all equipment when ON and OFF [watts]', nargs=2, type=float)
    p.add_argument('R', help='R-value constant [m^2 C/W]', type=float)
    p.add_argument('albedo', help='Cabinet albedo (is it bare metal, gray, white?)', type=float)

    p = p.parse_args()

    Qon = p.Qonoff[0]
    Qoff = p.Qonoff[1]

    for A in Areas:
        print('\nanalysis of ' + A['model'])
        A['air'] = 1*A['top'] + 2*A['side'] + 2*A['end']  # [m^2] roughly #neglect bottom side
        A['sun'] = A['top'] + A['side'] + A['end']  # [m^2] roughly

        print('enclosure area exposed to air is {:0.2f}'.format(A['air']) + ' m^2')
        print('enclosure area exposed to sun is {:0.2f}'.format(A['sun']) + ' m^2')
        print('Assuming albedo: {:0.1f}'.format(p.albedo))
        # http://books.google.com/books?id=PePq7o6mAbwC&lpg=PA282&ots=gOYd86tmHh&dq=house%20paint%20albedo&pg=PA283#v=onepage&q=house%20paint%20albedo&f=false
        print('Sign convention: negative watts is outgoing heat flux')
        print('-------------------------------------------')
        worstHeat(p.albedo, A, p.R, Qon)
        print('-------------------------------------------')
        worstCool(p.albedo, A, p.R, Qon)
        print('-------------------------------------------')
        SummerCool(p.albedo, A, p.R, Qoff)


def worstHeat(Albedo: float, A: Dict[str, float], R: float, Qequip: float):
    sel = 0
    # assume sun is below horizon 24 hours a day
    """http://weatherspark.com/averages/32940/1/Fairbanks-Alaska-United-States
     25th percentile -35C, 10th percentile -40C
    """
    Q = {'sun': 0., 'equip': Qequip}  # [W]
    T = {'out': -40, 'in': -10.}  # [C]]
    Q = calcQ(Q, A, sel, T, Albedo, R)

    print('10th percentile worst-case HEATing needs {:0.1f} watts / {:0.1f} BTU/hr.'.format(-Q['cooler'], -Q['cooler']*3.412))
    printQ(Q)


def worstCool(Albedo: float, A: Dict[str, float], R: float, Qequip: float):
    sel = 35
    """
    assume sun is at 35 degree elev
    neglects ground radation
    """
    """http://weatherspark.com/averages/32940/1/Fairbanks-Alaska-United-States
     25th percentile 18C, 10th percentile 21C
    """
    Q = {'sun': 850, 'equip': Qequip}  # [W]
    T = {'out': 20, 'in': 30.}  # [C]]
    Q = calcQ(Q, A, sel, T, Albedo, R)

    print('90th percentile worst-case COOLing needs {:0.1f} watts / {:0.1f} BTU/hr.'.format(Q['cooler'], Q['cooler']*3.412))
    printQ(Q)


def SummerCool(Albedo: float, A: Dict[str, float], R: float, Qequip: float):
    sel = 45
    # assume sun is at 45 degree elev, neglect cabinet albedo
    """http://weatherspark.com/averages/32940/1/Fairbanks-Alaska-United-States
     25th percentile 18C, 10th percentile 21C
    """
    Q = {'sun': 850., 'equip': Qequip}  # [W]
    T = {'out': 35., 'in': 40.}  # [C]
    Q = calcQ(Q, A, sel, T, Albedo, R)

    print('90th perc. Summer storage COOLing needs {:0.1f} watts / {:0.1f} BTU/hr.'.format(Q['cooler'], Q['cooler']*3.412))
    printQ(Q)


def calcQ(Q: Dict[str, float], A: Dict[str, float], sel: float,
          T: Dict[str, float], Albedo: float, R: float) -> Dict[str, float]:
    # invoke Lambert's Cosine Law
    Q['top'] = A['top'] * Q['sun'] * sin(radians(sel))  # max sun elev ~ 45 deg. mid summer
    Q['side'] = A['side'] * Q['sun'] * sin(radians(sel))  # worst case(?)
    Q['end'] = 0  # A['end']  * Qsun * sin(radians(45)) #consistent with angle used for top,side
    Q['solar'] = Q['top'] + Q['side'] + Q['end']  # figure only 1 side, 1 end lit up

    Q['ext'] = Q['solar']*(1-Albedo)
    Q['xfer'] = A['air'] / R * (T['out']-T['in'])

    Q['cooler'] = Q['ext'] + Q['xfer'] + Q['equip']  # [W]

    return Q


def printQ(Q: Dict[str, float]):
    print('Contributions:')
    print('Qext [Watts]: {:0.1f}'.format(Q['ext']))
    print('Qxfer [Watts]: {:0.1f}'.format(Q['xfer']))
    print('Qequip [Watts]: {:0.1f}'.format(Q['equip']))


# %%
if __name__ == '__main__':
    main()
