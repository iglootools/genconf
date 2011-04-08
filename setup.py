#!/usr/bin/env python
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
setup(
    name="genconf",
    version="0.2",
    author='Sami Dalouche',
    author_email='sami.dalouche@gmail.com',
    license='Apache-2.0',
    url='http://www.iglootools.org/genconf',
    description='A simple-to-use, template-based configuration file generator',
    long_description="genconf generates configuration files from a template." 
        "It is meant to be used inside software projects that need different config files"
        "depending on which environment is running for instance.",
    packages=find_packages(exclude=('tests', 'tests.*')),
    scripts=['gc'],
    include_package_data=True,
#    data_files=[('etc', ['etc/pymager-cherrypy.conf', 'etc/pymager.conf'])],
    test_suite="nose.collector",
    tests_require=['nose >= 0.11.1', 'mox >= 0.5.0'],
    install_requires=['PyYAML >= 3.09', 'Genshi >= 0.6', 'argparse >= 1.1'],
    # 'distribute >=0.6.15'
)
