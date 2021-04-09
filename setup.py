# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Miroslav Bauer @ CESNET.
#
# urnparse is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Python library for generating and parsing and RFC 8141 compliant uniform resource names (URN)."""

import os

from setuptools import find_packages, setup

readme = open('README.md').read()

OAREPO_VERSION = os.environ.get('OAREPO_VERSION', '3.3.0')

tests_require = [
]

extras_require = {
    'tests': [
        'pydocstyle',
        'isort',
        'check-manifest',
        'pytest'
    ],
}

setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
]

packages = find_packages(exclude="tests")

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('urnparse', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='urnparse',
    version=version,
    description=__doc__,
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Miroslav Bauer @ CESNET',
    author_email='bauer@cesnet.cz',
    url='https://github.com/oarepo/urnparse',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={},
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
    ],
)
