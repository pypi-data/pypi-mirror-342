# -*- coding: utf-8 -*-
"""
definitions of some global constants    
"""
# %%
import itertools
import warnings

import torch

# --- general configuration
# if True: raise error if wavelength not defined.
# if False: Warn and use closest match
ERROR_ON_WAVELENGTH_MISSMATCH = False


# --- default data types
DTYPE_FLOAT = torch.float32
DTYPE_COMPLEX = torch.complex64
# DTYPE_FLOAT = torch.float64
# DTYPE_COMPLEX = torch.complex128


# --- default torch device
DEFAULT_DEVICE = "cpu"


# --- default matplotlib colors. Generate with:
#     import matplotlib.colors as mcolors
#     COLORS_DEFAULT = [mcolors.to_hex(f"C{i}") for i in range(10)]
COLORS_DEFAULT = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
] * 10  # dirty hack: repeat enough times

# --- structure counter
STRUCTURE_IDS = itertools.cycle(range(100000000000))
