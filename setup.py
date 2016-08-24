#!/usr/bin/env python
from setuptools import setup
import subprocess

try:
    subprocess.call(['conda','install','--file','requirements.txt'])
except Exception as e:
    pass

setup(name='CommSitePlan',
      packages=['commsiteplan'],
	  description='utilities for planning comms sites and science outposts',
	  author='Michael Hirsch',
	  url='https://github.com/scienceopen/comm-site-planning',
	  install_requires=['pathlib2'],
      dependency_links = [],
	  )


