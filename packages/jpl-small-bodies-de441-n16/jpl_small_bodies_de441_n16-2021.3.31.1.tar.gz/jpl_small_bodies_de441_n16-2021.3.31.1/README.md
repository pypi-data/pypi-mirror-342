# jpl_small_bodies_de441_n16: JPL Small Bodies Ephemeris of 16 most massive asteroids for SPICE
#### A Python package by the Asteroid Institute, a program of the B612 Foundation

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue)](https://img.shields.io/badge/Python-3.7%2B-blue)
[![PyPI version](https://img.shields.io/pypi/v/jpl-small-bodies-de441-n16)](https://img.shields.io/pypi/v/jpl-small-bodies-de441-n16)
[![PyPi downloads](https://img.shields.io/pypi/dm/jpl-small-bodies-de441-n16)](https://img.shields.io/pypi/dm/jpl-small-bodies-de441-n16)  
[![Build and Test](https://github.com/B612-Asteroid-Institute/jpl_small_bodies_de441_n16/actions/workflows/build_test.yml/badge.svg)](https://github.com/B612-Asteroid-Institute/jpl_small_bodies_de441_n16/actions/workflows/build_test.yml)
[![Build, Test, & Publish](https://github.com/B612-Asteroid-Institute/jpl_small_bodies_de441_n16/actions/workflows/build_test_publish.yml/badge.svg)](https://github.com/B612-Asteroid-Institute/jpl_small_bodies_de441_n16/actions/workflows/build_test_publish.yml)  

This package ships the JPL Small Bodies DE441 kernal for the 16 most massive asteroids. [reference](https://ssd.jpl.nasa.gov/ftp/eph/small_bodies/asteroids_de441/SB441_IOM392R-21-005_perturbers.pdf).

**This is not an official JPL package**. It is an automatically generated mirror of the file so that it is
installable via `pip`.

## Installation

The latest version of the file can be install via pip:  
`pip install jpl-small-bodies-de441-n16`

## Usage
```python
import spiceypy as sp
from jpl_small_bodies_de441_n16 import de441_n16

sp.furnsh(de441_n16)
```

## Acknowledgment

This project makes use of data provided and maintained by the NASA Jet Propulsion Laboratory, California Institute of Technology.

