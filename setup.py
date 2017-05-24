#!/usr/bin/env python
req = ['nose','numpy','astropy','python-dateutil','matplotlib','seaborn']
import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:    
    pip.main(['install'] + req)
    
# %%
from setuptools import setup


setup(name='CommSitePlan',
      packages=['commsiteplan'],
	  description='utilities for planning comms sites and science outposts',
	  author='Michael Hirsch',
	  url='https://github.com/scivision/comm-site-planning',
	  )


