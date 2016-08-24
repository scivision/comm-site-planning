#!/usr/bin/env python
from datetime import datetime
from numpy import nan
from numpy.testing import assert_allclose,run_module_suite
#
from histutils.airMass import airmass
from histutils.compsolar import compsolar

def test_plotsolar():
    Irr,sunel,Whr = compsolar('pfisr',(None,None,None),
                          datetime(2015,7,1,0,0,0),5., 1, False)
    assert_allclose(Irr[[16,14,6],[105,155,174]], [ 437.853895,  412.637988,  414.4017],rtol=0.1) #astropy changes with revisions..
    assert_allclose(sunel[[6,14,6],[2,125,174]], [-33.154661, 4.35271 ,   9.325113],rtol=0.05) #py27 differes from py35


def test_airmass():
    theta=[-1.,38.]
    Irr,M,I0 = airmass(theta,datetime(2015,7,1,0,0,0))
    assert_allclose(Irr,[nan, 805.13538427])
    assert_allclose(M,[nan,  1.62045712])


if __name__ == '__main__':
    run_module_suite()