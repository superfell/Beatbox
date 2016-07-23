#!/usr/bin/python

# File: setup.py
# Author: Michael Stevens <mstevens@etla.org>
# Copyright (C) 2010

from setuptools import setup, find_packages


setup(
    name="beatbox",
    version="0.96",
    test_suite="beatbox",
    description="Makes the salesforce.com SOAP API easily accessible.",
    author="Simon Fell",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Intended Audience :: Developers",
    ],
    url="http://www.pocketsoap.com/beatbox/",
    packages=find_packages(),
)
