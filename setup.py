#!/usr/bin/env python3
#
# Dhesant Nakka
# dhesant.nakka@gmail.com
""" A setuptools based setup module. """

from pathlib import Path
from setuptools import setup

here = Path(__file__).parent.resolve()

setup(
    name="apcups2telegraf",
    author="Dhesant Nakka",
    author_email="dhesant.nakka@gmail.com",
    py_modules=["apcstatus"],
    entry_points={"console_scripts": ["apcstatus=apcstatus:main"]},
    python_requires=">=3.6, <4",
    install_requires=["python-dateutil>=2.8, <3", "pytz"],
    version="0.1.1",
)
