#!/usr/bin/env python
from datetime import datetime
from numpy.testing import assert_allclose,run_module_suite
#
from commsiteplan import airmass, compsolar

def test_plotsolar():
    Irr,sunel = compsolar('pfisr',None,
                          datetime(2015,7,1,0,0,0),5., 1)
    assert_allclose(Irr['Irr'][16,105], 439.888426,rtol=0.1) #astropy changes with revisions..
    assert_allclose(sunel[6,174], 9.325113,rtol=0.05) #py27 differes from py35


def test_airmass():
    theta=[-1.,38.]
    Irr = airmass(theta,datetime(2015,7,1,0,0,0))
    assert_allclose(Irr['Irr'], 805.13538427)
    assert_allclose(Irr['Am'],  1.62045712)


if __name__ == '__main__':
    run_module_suite()
