#!/usr/bin/env python
from setuptools import setup

setup(
    name='intercom',
    version='0.0.1',
    url='https://github.com/alexhanson/intercom',
    license='ISC License',
    python_requires='>=3.7',
    install_requires=[
        'click==7.0',
        'CherryPy==18.1.2',
        'Jinja2==2.10.1',
        'pytz==2019.2',
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
