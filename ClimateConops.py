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
Areas = [
    {'side': 0.45, 'end': 0.35, 'top': 0.45, 'model': 'Zarges'},
    {'side': 0.51, 'end': 0.50, 'top': 0.41, 'model': 'OD-30DXC'},
    {'side': 1.40, 'end': 1.40, 'top': 0.8, 'model': 'Compact greenhouse'}]

COLDEST_OUTSIDE_TEMP_C = -20.
COLDEST_INSIDE_TEMP_C = 0.
SOLAR_IRR = 850.  # Watts
WARMEST_OUTSIDE_TEMP_C = 20.
WARMEST_INSIDE_TEMP_C = 30.


def main():
    p = ArgumentParser(description='very simple steady state thermodynamic enclosure analysis')
    p.add_argument('Qon', help='Internal heat generated [watts]', type=float)
    p.add_argument('R', help='R-value constant [m^2 C/W]', type=float)
    p.add_argument('albedo', help='Cabinet albedo (is it bare metal, gray, white?)', type=float)

    p = p.parse_args()

    Qon = p.Qon

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
        if not A['model'].endswith('greenhouse'):
            print('-------------------------------------------')
            worstCool(p.albedo, A, p.R, Qon)


def worstHeat(Albedo: float, A: Dict[str, float], R: float, Qequip: float):
    """
    http://weatherspark.com/averages/32940/1/Fairbanks-Alaska-United-States
     25th percentile -35C, 10th percentile -40C
    """
    NIGHT_SOLAR_ELEV = 0.
    NIGHT_SOLAR_IRR = 0.

    Q = {'sun': NIGHT_SOLAR_IRR, 'equip': Qequip}  # [W]
    T = {'out': COLDEST_OUTSIDE_TEMP_C, 'in': COLDEST_INSIDE_TEMP_C}  # [C]]
    Q = calcQ(Q, A, NIGHT_SOLAR_ELEV, T, Albedo, R)

    print(f'for outside temp C {COLDEST_OUTSIDE_TEMP_C} and inside temp C {COLDEST_INSIDE_TEMP_C}:')
    print(f'  HEATing needs: {-Q["cooler"]:0.1f} watts / {-Q["cooler"]*3.412:0.1f} BTU/hr.')
    printQ(Q)


def worstCool(Albedo: float, A: Dict[str, float], R: float, Qequip: float):
    """
    assume sun is at 35 degree elev
    neglects ground radation

    http://weatherspark.com/averages/32940/1/Fairbanks-Alaska-United-States
     25th percentile 18C, 10th percentile 21C
    """
    SOLAR_ELEV = 35.  # Degrees

    Q = {'sun': SOLAR_IRR, 'equip': Qequip}  # [W]
    T = {'out': WARMEST_OUTSIDE_TEMP_C, 'in': WARMEST_INSIDE_TEMP_C}  # [C]]
    Q = calcQ(Q, A, SOLAR_ELEV, T, Albedo, R)

    print('90th percentile worst-case COOLing needs {:0.1f} watts / {:0.1f} BTU/hr.'.format(Q['cooler'], Q['cooler']*3.412))
    printQ(Q)


def SummerCool(Albedo: float, A: Dict[str, float], R: float, Qequip: float):
    """
    assume sun is at 45 degree elev, neglect cabinet albedo

    http://weatherspark.com/averages/32940/1/Fairbanks-Alaska-United-States
     25th percentile 18C, 10th percentile 21C
    """
    SOLAR_ELEV = 45.  # Degrees

    Q = {'sun': SOLAR_IRR, 'equip': Qequip}  # [W]
    T = {'out': WARMEST_OUTSIDE_TEMP_C, 'in': WARMEST_INSIDE_TEMP_C}  # [C]
    Q = calcQ(Q, A, SOLAR_ELEV, T, Albedo, R)

    print('Summer storage COOLing needs {:0.1f} watts / {:0.1f} BTU/hr.'.format(Q['cooler'], Q['cooler']*3.412))
    printQ(Q)


def calcQ(Q: Dict[str, float], A: Dict[str, float], sel: float,
          T: Dict[str, float], Albedo: float, R: float) -> Dict[str, float]:
    """
    calculate heat flux
    """
# %% invoke Lambert's Cosine Law
    Qtop = A['top'] * Q['sun'] * sin(radians(sel))  # max sun elev ~ 45 deg. mid summer
    Qside = A['side'] * Q['sun'] * sin(radians(sel))  # worst case(?)
    Qend = 0.  # A['end']  * Qsun * sin(radians(45)) #consistent with angle used for top,side
    Q['solar'] = Qtop + Qside + Qend  # figure only 1 side, 1 end lit up

    Q['ext'] = Q['solar'] * (1-Albedo)
    Q['xfer'] = A['air'] / R * (T['out'] - T['in'])

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
