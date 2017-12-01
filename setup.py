#!/usr/bin/env python
install_requires= ['numpy','astropy','python-dateutil','matplotlib']
tests_require=['nose','coveralls']
# %%
from setuptools import setup


setup(name='CommSitePlan',
      packages=['commsiteplan'],
	  description='utilities for planning comms sites and science outposts',
	  author='Michael Hirsch',
	  url='https://github.com/scivision/comm-site-planning',
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'plot':['seaborn'],
                      'tests':tests_require},
      python_requires='>=2.7',
	  )


