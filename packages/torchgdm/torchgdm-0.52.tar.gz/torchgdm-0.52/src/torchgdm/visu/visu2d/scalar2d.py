# encoding=utf-8
"""
2D visualization tools for vector fields
"""
# %%
import copy
import warnings

import torch

from torchgdm.constants import COLORS_DEFAULT
from torchgdm.tools.misc import to_np
from torchgdm.visu.visu2d._tools import (
    _get_axis_existing_or_new,
    _get_closest_slice_level,
    _interpolate_to_grid,
    _automatic_projection,
    _apply_projection,
)


def field_intensity(field, illumination_index=0, whichfield="e", **kwargs):
    """2D colorplot of field intensity"""
    if whichfield.lower() == "e":
        f = field.get_efield_intensity()[illumination_index]
    else:
        f = field.get_hfield_intensity()[illumination_index]

    return _scalarfield(f, field.positions, **kwargs)


def field_amplitude(
    field,
    illumination_index=0,
    whichfield="e",
    complex_part="re",
    field_component="x",
    **kwargs,
):
    """2D colorplot of a field amplitude component"""
    if whichfield.lower() == "e":
        f = field.efield[illumination_index]
    else:
        f = field.hfield[illumination_index]

    if complex_part.lower() in ["re", "real"]:
        f = f.real
    elif complex_part.lower() in ["im", "imag"]:
        f = f.imag
    else:
        raise ValueError("Unknown complex part. Use either 're' or 'im'.")

    if field_component.lower() == "x":
        f = f[:, 0]
    elif field_component.lower() == "y":
        f = f[:, 1]
    elif field_component.lower() == "z":
        f = f[:, 2]
    else:
        raise ValueError("Unknown field_component. Use either 'x', 'y' or 'z'.")

    return _scalarfield(f, field.positions, **kwargs)


def _scalarfield(
    field_scalars,
    positions,
    projection="auto",
    slice_level=None,
    interpolation_grid_data="linear",
    set_ax_aspect=True,
    **kwargs,
):
    """2D colorplot of a scalar field

    plot nearfield list as 2D vector plot, using matplotlib's `quiver`.
    `kwargs` are passed to `pyplot.quiver`

    Args:
        field_scalars (torch.Tensor): list of scalar values
        positions (torch.Tensor): list of (x,y,z) coordinates
        projection (str, optional): Which 2D projection to plot: "auto", "XY", "YZ", "XZ". Defaults to "auto".
        slice_level (float, optional): depth where to slice. eg if projection=='XY', slice_level=10 will take only values where Z==10. If no positions exist with the selected coordinate value, take the closest existing value. Defaults to None.
        interpolation_grid_data (str, optional): interpolation method for scipy `grid_data`. Can be 'linear' or 'nearest'. See `scipy.interpolate.griddata` for details. Defaults to "linear".
        set_ax_aspect (bool, optional): set aspect of matplotlib axes to "equal". Defaults to True.

    Returns:
        output of matplotlib's `quiver`
    """
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np

    if type(positions) == dict:
        positions = positions["r_probe"]

    assert len(field_scalars) == len(positions)

    # - to numpy, take real or imag part
    s = to_np(field_scalars).real
    _p = to_np(positions).real

    # - select projection
    if projection.lower() == "auto":
        projection = _automatic_projection(_p)
    p, levels = _apply_projection(_p, projection)

    # - optional slicing
    if slice_level is not None:
        slice_level = _get_closest_slice_level(levels, slice_level)
        p = p[(levels == slice_level)]
        s = s[(levels == slice_level)]

    # - interpolate grid data
    map_2d, extent = _interpolate_to_grid(
        p[:, 0], p[:, 1], s, interpolation=interpolation_grid_data
    )

    # - prep matplotlib, axes
    ax, show = _get_axis_existing_or_new()
    if set_ax_aspect:
        ax.set_aspect("equal")

    # plot
    im = ax.imshow(map_2d, extent=extent, **kwargs)

    if show:
        plt.show()

    return im
