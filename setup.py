#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'Readme.md')) as f:
        README = f.read()

        REQUIREMENTS = [
            'setuptools>17.1',
            'requests>=2.6.0',
            'mock>=1.0.1',
            'nose>=1.3.4',
            'nose-cov',
            'nose-mocha-reporter',
            'coverage',
            'tox>=1.9.0',
            'flake8>=2.4.0',
            'Sphinx>=1.3',
            'sphinx_rtd_theme>=0.1.7',
        ]

        setup(
                name='setup-virtual-machine',
                version='0.0.1',
                description='python-server-setup',
                long_description=README,
                author='James Michel DuPont',
                author_email='jamesmikedupont@gmail.com',
                url='https://github.com/rpappalax/python-project-template',
                license="GPL3",
                install_requires=REQUIREMENTS,
                keywords=['setup.py', 'project', 'tox'],
                packages=find_packages(),
                classifiers=[
                            'Programming Language :: Python',
                            'Programming Language :: Python :: 2.7',
                            'Programming Language :: Python :: 3.3',
                ],
                entry_points={
                    #'console_scripts': ['demo = demo.demo_handler:main']
                },
        )
