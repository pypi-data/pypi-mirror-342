# naif_eop_predict: NAIF Longterm Prediction Earth Orientation Parameters Kernel for SPICE
#### A Python package by the Asteroid Institute, a program of the B612 Foundation

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue)](https://img.shields.io/badge/Python-3.7%2B-blue)
[![PyPI version](https://img.shields.io/pypi/v/naif-eop-predict)](https://img.shields.io/pypi/v/naif-eop-predict)
[![PyPi downloads](https://img.shields.io/pypi/dm/naif-eop-predict)](https://img.shields.io/pypi/dm/naif-eop-predict)  
[![Build and Test](https://github.com/B612-Asteroid-Institute/naif_eop_predict/actions/workflows/build_test.yml/badge.svg)](https://github.com/B612-Asteroid-Institute/naif_eop_predict/actions/workflows/build_test.yml)
[![Build, Test, & Publish](https://github.com/B612-Asteroid-Institute/naif_eop_predict/actions/workflows/build_test_publish.yml/badge.svg)](https://github.com/B612-Asteroid-Institute/naif_eop_predict/actions/workflows/build_test_publish.yml)  

This package ships the Navigation and Ancillary Information Facility's low accuracy, longterm prediction Earth orientation parameters (EOP) [kernel](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_200101_990827_predict.bpc).

**This is not an official NAIF package**. It is an automatically generated mirror of the file so that it is
installable via `pip`. 

The current version of the file released on 2024 AUG 28 spans the following times: 2020 JAN 01 00:01:09.183 TDB - 2099 AUG 27 00:01:09.182 TDB

## Installation

The latest version of the file can be installed via pip:  
`pip install naif-eop-predict`

## Usage
```python
import spiceypy as sp
from naif_eop_predict import eop_predict

sp.furnsh(eop_predict)
```

## Acknowledgment

This project makes use of data provided and maintained by the Navigation and Ancillary Information Facility (NAIF). 

### References
[1] Acton, C.H.; "Ancillary Data Services of NASA's Navigation and Ancillary Information Facility;" Planetary and Space Science, Vol. 44, No. 1, pp. 65-70, 1996.
DOI 10.1016/0032-0633(95)00107-7  
[2] Charles Acton, Nathaniel Bachman, Boris Semenov, Edward Wright; A look toward the future in the handling of space science mission geometry; Planetary and Space Science (2017);
DOI 10.1016/j.pss.2017.02.013
