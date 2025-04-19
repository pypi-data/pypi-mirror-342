# encoding=utf-8
"""
internal tools for 2D visualizations
"""
# %%
import warnings

import torch

from torchgdm.tools.misc import to_np


def _get_axis_existing_or_new():
    import matplotlib.pyplot as plt

    if len(plt.get_fignums()) == 0:
        show = True
        ax = plt.subplot()
    else:
        show = False
        ax = plt.gca()
    return ax, show


def _get_closest_slice_level(levels, slice_level, limit_level=9999):
    import numpy as np

    slice_level_closest = np.unique(levels)[
        np.argmin(np.abs(np.unique(levels) - slice_level))
    ]
    if slice_level_closest != slice_level:
        if np.abs(slice_level) != limit_level:
            warnings.warn(
                "slice level at {}nm contains no meshpoints. Using closest level containing meshpoint at {}nm".format(
                    slice_level, slice_level_closest
                )
            )
    return slice_level_closest


def _automatic_projection(positions):
    import numpy as np

    pos_np = to_np(positions)

    if len(np.unique(pos_np[:, 2])) == 1:
        projection = "xy"
    elif len(np.unique(pos_np[:, 1])) == 1:
        projection = "xz"
    elif len(np.unique(pos_np[:, 0])) == 1:
        projection = "yz"
    else:
        # fallback
        warnings.warn("3D data. Falling back to XY projection...")
        projection = "xy"

    return projection


def _interpolate_to_grid(
    x,
    y,
    s,
    n_x=None,
    n_y=None,
    interpolation="nearest",
    fill_value="nan",
    return_grid=False,
    **kwargs
):
    """wrapper to scipy.interpolate.griddata

    List of X/Y/Z tuples to 2D x/y Grid with z as intensity value

    Parameters
    ----------
    x, y : np.array
        1D arrays containing x and y positions of the data

    s : np.array
        scalar values corresponding at each (x,y)-coordinate.

    n_x, n_y : int, optional
        number of points in X/Y direction for interpolation
        default: Number of unique occuring x/y elements

    interpolation : str, default: 'nearest'
        interpolation method for grid, passed to `scipy.griddata`

    **kwargs are passed to `scipy.interpolate.griddata`

    Returns
    -------
    map_ip : np.ndarray
        2d array with interpolated values in x/y plane

    extent : tuple
        x/y extent of array map as (x0, x1, y0, y1)

    """
    import numpy as np
    from scipy.interpolate import griddata

    if fill_value.lower == "nan":
        fill_value = np.nan

    # - determine limits and nr of steps for 2D grid interpolation
    x0, x1 = float(np.min(x)), float(np.max(x))
    y0, y1 = float(np.min(y)), float(np.max(y))
    extent = [x0, x1, y0, y1]

    if n_x is None:
        n_x = len(np.unique(x))
    if n_y is None:
        n_y = len(np.unique(y))

    # perform interpolation on regular grid
    grid_x, grid_y = np.meshgrid(np.linspace(x0, x1, n_x), np.linspace(y0, y1, n_y))
    map_ip = griddata(
        np.transpose([x, y]),
        s,
        (grid_x.T, grid_y.T),
        method=interpolation,
        fill_value=fill_value,
        **kwargs,
    )
    map_ip = np.flipud(map_ip.T)  # match convention: origin lower left
    if return_grid:
        return map_ip, extent, grid_x, grid_y
    else:
        return map_ip, extent


def _apply_projection(pos, projection):

    if projection.lower() == "xy":
        p = pos[:, [0, 1]]
        levels = pos[:, 2]
    elif projection.lower() == "yz":
        p = pos[:, [1, 2]]
        levels = pos[:, 0]
    elif projection.lower() == "xz":
        p = pos[:, [0, 2]]
        levels = pos[:, 1]
    else:
        raise ValueError("Invalid projection argument!")

    return p, levels


def _apply_projection_to_vectorfield(vec, pos, projection, complex_part=None):

    if complex_part is None:
        vec_scalar = vec
    elif complex_part.lower() == "real":
        vec_scalar = vec.real
    elif complex_part.lower() == "imag":
        vec_scalar = vec.imag
    else:
        raise ValueError(
            "Error: Unknown `complex_part` argument. Must be either 'real' or 'imag'."
        )

    v, _ = _apply_projection(vec_scalar, projection)
    p, levels = _apply_projection(pos, projection)

    return v, p, levels


def _optimize_alpha_value(
    pos2d_exp, alpha_step_limit=1e-3, alpha_init=0.0, time_limit=5.0
):
    """find best alpha_value that still returns an alphashape"""
    import logging
    import time
    import alphashape

    alpha_value = alpha_init
    step = 0.1
    t0 = time.time()

    # solver loop
    original_log_level = logging.getLogger().getEffectiveLevel()
    logging.disable(logging.WARN)
    while 1:
        _ga = alphashape.alphashape(pos2d_exp, alpha_value + step)
        print(alpha_value + step,_ga.geom_type)
        if _ga.geom_type not in ["Polygon", "MultiPolygon"]:
            step /= 2  # no solution: reduce search step
            if step < alpha_step_limit:
                break # step limit reached
            if time.time() - t0 > time_limit:
                break # time limit reached
        else:
            # solution found, update step
            alpha_value += step

    print(alpha_value,_ga.geom_type)
    logging.disable(original_log_level)
    return alpha_value


def _alpha_shape(points: torch.Tensor, alpha=1.0, only_outer=True):
    """Compute the alpha shape (concave hull) of a set of points.

    from : https://karobben.github.io/2022/03/07/Python/point_outline/

    Args:
        points (torch.Tensor): List of 2D points. shape (n,2) points.
        alpha (float, optional): alpha value. Defaults to 1.0.
        only_outer (bool, optional): whether to keep only the outer border or also inner edges. Defaults to True.

    Returns:
        torch.Tensor: set of (i,j) pairs representing edges of the alpha-shape. (i,j) are the indices in the points array.
    """
    from scipy.spatial import Delaunay

    assert points.shape[0] > 3, "Need at least four points"

    def add_edge(edges, i, j):
        """
        Add an edge between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            assert (j, i) in edges, "Can't go twice over same directed edge right?"
            if only_outer:
                # if both neighboring triangles are in shape, it's not a boundary edge
                edges.remove((j, i))
            return
        edges.add((i, j))

    tri = Delaunay(points)

    edges = set()
    # Loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.simplices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]
        # Computing radius of triangle circumcircle
        # www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
        a = torch.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
        b = torch.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
        c = torch.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
        s = (a + b + c) / 2.0
        area = torch.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)
        if circum_r < alpha:
            add_edge(edges, ia, ib)
            add_edge(edges, ib, ic)
            add_edge(edges, ic, ia)
    return edges
