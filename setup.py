#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='ShowStopper',
    version='0.1.0',
    description="Audio for dramatic productions",
    long_description=readme + '\n\n' + history,
    author="Paul Knox-Kennedy",
    author_email='paul@knox-kennedy.me.uk',
    url='https://github.com/pdkk/ShowStopper',
    packages=[
        'ShowStopper',
    ],
    package_dir={'ShowStopper':
                 'ShowStopper'},
    include_package_data=True,
    package_data={'ShowStopper':['images/*.png']},
    install_requires=requirements,
    entry_points={
	    'gui_scripts': [
		    'ShowStopper = ShowStopper.ShowStopper:main',
		    ]
	    },
    license="BSD",
    zip_safe=False,
    keywords='ShowStopper',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
