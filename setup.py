#!/usr/bin/env python3

from setuptools import setup

setup(name='hues',
      version='0.1',
      description='A Philips hue scheduler',
      url='https://github.com/acwatkins/hues',
      author='Adam Watkins',
      author_email='acwatkins@gmail.com',
      license='GPL3',
      modules=['hues'],
      install_requires = ['phue>=0.8'])
