#!/usr/bin/env python
from datetime import datetime
from numpy.testing import assert_allclose,run_module_suite
#
from commsiteplan import airmass, compsolar

def test_plotsolar():
    Irr,sunel = compsolar('pfisr',5., 4,2018)

    assert_allclose(Irr['Irr'][5,105], 810.615382,rtol=0.01) #astropy changes with revisions..
    assert_allclose(sunel[4,174], 21.900123,rtol=0.05) #py27 differes from py35
    assert_allclose(Irr['Whr'][105], 6514.7805,rtol=0.01)

def test_airmass():
    theta=[-1.,38.]
    Irr = airmass(theta,datetime(2015,7,1,0,0,0))
    assert_allclose(Irr['Irr'], 805.13538427)
    assert_allclose(Irr['Am'],  1.62045712)


if __name__ == '__main__':
    run_module_suite()
