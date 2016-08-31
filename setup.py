#!/usr/bin/env python
from setuptools import setup

setup(
    name='intercom',
    version='0.0.1',
    url='https://github.com/alexhanson/intercom',
    license='ISC License',
    install_requires=[
        'click==6.6',
        'CherryPy==7.1.0',
        'Jinja2==2.8',
        'pytz==2016.6.1',
    ],
    packages=[
        'intercom',
    ],
    package_data={
        'intercom': ['templates/*'],
    },
    entry_points={
        'console_scripts': ['intercom = intercom.__main__:main'],
    },
)
