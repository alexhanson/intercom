#!/usr/bin/env python
from setuptools import setup

setup(
    name='intercom',
    version='0.0.1',
    url='https://github.com/alexhanson/intercom',
    license='ISC License',
    python_requires='>=3.8',
    install_requires=[
        'click==7.1.2',
        'CherryPy==18.6.0',
        'Jinja2==2.11.3',
        'pytz==2021.1',
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
