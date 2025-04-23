# naif_earth_itrf93: NAIF Earth Body-fixed Reference Frame/Body Association Kernel for SPICE
#### A Python package by the Asteroid Institute, a program of the B612 Foundation

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue)](https://img.shields.io/badge/Python-3.7%2B-blue)
[![PyPI version](https://img.shields.io/pypi/v/naif-earth-itrf93)](https://img.shields.io/pypi/v/naif-earth-itrf93)
[![PyPi downloads](https://img.shields.io/pypi/dm/naif-earth-itrf93)](https://img.shields.io/pypi/dm/naif-earth-itrf93)  
[![Build and Test](https://github.com/B612-Asteroid-Institute/naif_earth_itrf93/actions/workflows/build_test.yml/badge.svg)](https://github.com/B612-Asteroid-Institute/naif_earth_itrf93/actions/workflows/build_test.yml)
[![Build, Test, & Publish](https://github.com/B612-Asteroid-Institute/naif_earth_itrf93/actions/workflows/build_test_publish.yml/badge.svg)](https://github.com/B612-Asteroid-Institute/naif_earth_itrf93/actions/workflows/build_test_publish.yml)  

This package ships the Navigation and Ancillary Information Facility's Earth Body-fixed Reference Frame/Body Association [kernel](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/planets/earth_assoc_itrf93.tf).

**This is not an official NAIF package**. It is an automatically generated mirror of the file so that it is
installable via `pip`.

## Installation

The latest version of the file can be installed via pip:  
`pip install naif-earth-itrf93`

## Usage
```python
import spiceypy as sp
from naif_earth_itrf93 import earth_itrf93

sp.furnsh(earth_itrf93)
```

## Acknowledgment

This project makes use of data provided and maintained by the Navigation and Ancillary Information Facility (NAIF). 

### References
[1] Acton, C.H.; "Ancillary Data Services of NASA's Navigation and Ancillary Information Facility;" Planetary and Space Science, Vol. 44, No. 1, pp. 65-70, 1996.
DOI 10.1016/0032-0633(95)00107-7  
[2] Charles Acton, Nathaniel Bachman, Boris Semenov, Edward Wright; A look toward the future in the handling of space science mission geometry; Planetary and Space Science (2017);
DOI 10.1016/j.pss.2017.02.013
