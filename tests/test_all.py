#!/usr/bin/env python
from datetime import datetime
import pytest
#
from commsiteplan import airmass, compsolar


def test_compsolar():
    Irr = compsolar([65, -148], 5., 4, 2018)

    assert Irr['Irr'][5, 105] == pytest.approx(810.615382, rel=0.01)  # astropy changes with revisions..
    assert Irr['sunel'][4, 174] == pytest.approx(21.900123, rel=0.05)  # py27 differes from py35
    assert Irr['Whr'][105] == pytest.approx(6514.7805, rel=0.01)


def test_airmass():
    theta = [-1., 38.]
    Irr = airmass(theta, datetime(2015, 7, 1, 0, 0, 0))
    assert Irr['Irr'] == pytest.approx(805.13538427)
    assert Irr['Am'] == pytest.approx(1.62045712)


if __name__ == '__main__':
    pytest.main([__file__])
