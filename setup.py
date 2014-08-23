#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name='pybargain_protocol',
    version='0.0.1',
    description='Python Bargaining Protocol Library',
    long_description=open('README.md').read(),
    author='laurentmt',
    maintainer='laurentmt',
    url='http://www.github.com/LaurentMT/pybargain_protocol',
    packages=find_packages(exclude=['tests']),
    install_requires=['bitcoin>=1.1.8'])
