#!/usr/bin/env python
install_requires= ['numpy','astropy','python-dateutil','xarray','matplotlib']
tests_require=['pytest','nose','coveralls']
# %%
from setuptools import setup, find_packages


setup(name='CommSitePlan',
      packages=find_packages(),
      version='0.5.0',
	  description='utilities for planning comms sites and science outposts',
	  long_description=open('README.rst').read(),
	  author='Michael Hirsch, Ph.D.',
	  url='https://github.com/scivision/comm-site-planning',
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'plot':['seaborn'],
                      'tests':tests_require},
      python_requires='>=3.6',
      classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: Science/Research',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      ],
	  )


