#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Explicitly exclude the monitoring module as it's still under development
packages = find_packages(exclude=["merit.monitoring", "merit.monitoring.*"])

if __name__ == "__main__":
    setup(packages=packages)
