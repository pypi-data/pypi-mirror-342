# PyTurbo
---
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/documentation-latest-blue)](https://github.com/aayouche/pyturbo_sf)

<p align="center">
<img src="docs/pyturbo_logo.png" alt="PyTurbo Logo" width="400"/>
</p>

# Overview
---
PyTurbo_SF is a Python package for efficient structure function calculations in 1D, 2D, and 3D data. The package provides optimized implementations for analyzing turbulent flows and other spatially or temporally varying fields. With advanced bootstrapping techniques and adaptive binning, PyTurbo_SF can handle large datasets while maintaining statistical accuracy.

# Features
---
- Fast structure function calculations in 1D, 2D, and 3D
- Optimized memory usage for large datasets
- Advanced bootstrapping with adaptative sampling indices
- Multiple structure function types: longitudinal, transverse, scalar, and combined
- Isotropic averaging for 2D and 3D data
- Parallel processing for improved performance
- Automatic convergence detection based on a standard error threshold (in physical units)
- Comprehensive statistical analysis


**For detailed documentation and examples, see the [PyTurbo_SF documentation](https://github.com/aayouche/PyTurbo).**

# Installation
---
The easiest method to install PyTurbo_SF is with [pip](https://pip.pypa.io/):

```console
$ pip install pyturbo_sf
```

You can also fork/clone this repository to your local machine and install it locally with pip as well:

```console
$ pip install .
```

# Quickstart
---
Once PyTurbo_SF is installed, you can perform structure function calculations on your data:
```
import numpy as np
import xarray as xr
import pyturbo_sf

# Create sample 2D dataset
nx, ny = 256, 256
x = np.linspace(0, 2*np.pi, nx)
y = np.linspace(0, 2*np.pi, ny)
X, Y = np.meshgrid(x, y)

# Create velocity components
u = np.sin(X) * np.cos(Y)
v = -np.cos(X) * np.sin(Y)

# Create xarray Dataset with 2D coordinates
ds = xr.Dataset(
    data_vars={
        "u": (["y", "x"], u),
        "v": (["y", "x"], v),
    },
    coords={
        "x": (["y", "x"], X),
        "y": (["y", "x"], Y),
    }
)

# Define logarithmic bins
bins = {
    'x': np.logspace(-2, 0, 20),
    'y': np.logspace(-2, 0, 20)
}

# Calculate 2D structure function
sf_result = pyturbo_sf.bin_sf_2d(
    ds=ds,
    variables_names=["u", "v"],
    order=2,
    bins=bins,
    fun='longitudinal',
    bootsize=32,
    initial_nbootstrap=50,
    max_nbootstrap=200,
    convergence_eps=0.1
)

# Calculate isotropic structure function
sf_iso = pyturbo_sf.get_isotropic_sf_2d(
    ds=ds,
    variables_names=["u", "v"],
    order=2,
    bins={'r': np.logspace(-2, 0, 20)},
    fun='longitudinal'
)
```


"Can I use PyTurbo_SF with my data?"
---
PyTurbo_SF is designed to work with various types of data, provided they can be organized into an xarray Dataset with proper dimensional information. It supports:

	- Turbulence simulation data
	- Fluid flow measurements
	- Meteorological and oceanographic data
	- Time series
	- Any structured or unstructured 1D, 2D, or 3D data in cartesian Grid

If you are uncertain about using PyTurbo_SF with your specific dataset, please open an issue or start a discussion in the GitHub repository.

# Performance Benchmarks
---
PyTurbo_SF is optimized for both speed and memory efficiency. Our benchmarks show computational complexity scaling as O(N log N), making it suitable for large datasets.
<p align="center">
<img src="docs/performance_benchmark.png" alt="PyTurbo Performance Benchmarks" width="400"/>
</p>

# Contributing
---
This project welcomes contributions and suggestions. Feel free to open an issue, submit a pull request, or contact the maintainers directly.

# Funding Acknowledgement
---
This software package is based upon work supported by the US Department of Energy grant DE-SC0024572. 

Any opinions, findings, and conclusions or recommendations expressed in this package are those of the authors and do not necessarily reflect the views of the US Department of Energy.

# References
---
- Pearson, B. et al., 2021: _Advective structure functions in anisotropic two-dimensional turbulence._ Journal of Fluid Mechanics.
- Lindborg, E. 2008: _Third-order structure function relations for quasi-geostrophic turbulence._ Journal of Fluid Mechanics.
- Kolmogorov, A.N. 1941: The local structure of turbulence in incompressible viscous fluid for very large Reynolds numbers. Proc. R. Soc. Lond. A.
- Frisch, U. 1995: Turbulence: The Legacy of A.N. Kolmogorov. Cambridge University Press.
- Pope, S.B. 2000: Turbulent Flows. Cambridge University Press.

