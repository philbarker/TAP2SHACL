#!/usr/bin/env python

from distutils.core import setup

setup(name='TAP2SHACL',
      version='0.1.1',
      description='DC TAP to SHACL cnoverter',
      author='Phil Barker',
      author_email='phil.barker@pjjk.co.uk',
      url='https://github.com/philbarker/TAP2SHACL',
      packages=['tap2shacl'],
      dependency_links=[
        "git+https://github.com/philbarker/AP2SHACL#egg=ap2shacl"
        "git+https://github.com/philbarker/APClasses#egg=AP"
        "git+https://github.com/philbarker/TAP2AP#egg=TAP2AP"
        "https://github.com/dcmi/dctap-python/archive/main.zip"
      ]
     )
