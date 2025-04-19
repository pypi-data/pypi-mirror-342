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
from torchgdm.tools.misc import get_closest_wavelength
from torchgdm.visu.visu2d._tools import (
    _get_axis_existing_or_new,
    _get_closest_slice_level,
    _automatic_projection,
    _interpolate_to_grid,
    _apply_projection_to_vectorfield,
)


def vectorfield(field, illumination_index=0, whichfield="e", **kwargs):
    """quiver plot of 2D projection of 3D vectorsfield"""
    if whichfield.lower() == "e":
        f = field.efield[illumination_index]
    else:
        f = field.hfield[illumination_index]

    return _vectorfield(f, field.positions, **kwargs)


def streamlines_energy_flux(field, illumination_index=0, **kwargs):
    """plot energy flux streamlines"""
    f = field.get_energy_flux()[illumination_index]

    return _streamlines(f, field.positions, **kwargs)


def vectorfield_inside(sim, wavelength, illumination_index, whichfield="e", **kwargs):
    """quiver plot of 2D projection of 3D vectorfield inside structure"""
    wl = get_closest_wavelength(sim, wavelength)

    if len(sim.fields_inside) == 0:
        raise ValueError("No fields present. Run simulation first.")

    if illumination_index >= len(sim.fields_inside[wl].efield):
        raise ValueError(
            "Specified `illumination_index` out of range. Use an existing illumination."
        )

    if whichfield.lower() == "e":
        f = sim.fields_inside[wl].efield[illumination_index]
    else:
        f = sim.fields_inside[wl].hfield[illumination_index]

    return _vectorfield(f, sim.get_all_positions(), **kwargs)


def _vectorfield(
    field_vectors,
    positions,
    projection="auto",
    complex_part="real",
    slice_level=None,
    scale=10.0,
    sort_by_length=True,
    override_max_vector_length=False,
    cmap=None,
    set_ax_aspect=True,
    cmin=0.3,
    each_n_points=1,
    **kwargs,
):
    """quiver plot of 2D projection of 3D vectorsfield

    plot nearfield list as 2D vector plot, using matplotlib's `quiver`.
    `kwargs` are passed to `pyplot.quiver`

    Parameters
    ----------
    field_vectors : list of 3- or 6-tuples
        Nearfield definition. `np.array`, containing 6-tuples:
        (X,Y,Z, Ex,Ey,Ez), the field components being complex (use e.g.
        :func:`.tools.get_field_as_list`).
        Optionally can also take a list of 3-tuples (Ex, Ey, Ez),
        in which case the structure must be provided via the `struct` kwarg.

    positions : list or :class:`.core.simulation`, optional
        optional structure definition (necessary if field is supplied in
        3-tuple form without coordinates). Either `simulation` description
        object, or list of (x,y,z) coordinate tuples

    projection : str, default: 'auto'
        Which 2D projection to plot: "auto", "XY", "YZ", "XZ"

    complex_part : str, default: 'real'
        Which part of complex field to plot. Either 'real' or 'imag'.

    slice_level: float, default: `None`
        optional value of depth where to slice. eg if projection=='XY',
        slice_level=10 will take only values where Z==10.
            - slice_level = `None`, plot all vectors one above another without slicing.
            - slice_level = -9999 : take minimum value in field-list.
            - slice_level = 9999 : take maximum value in field-list.

    scale : float, default: 10.0
        optional vector length scaling parameter

    cmap : matplotlib colormap, default: `cm.Blues`
        matplotlib colormap to use for arrows (color scaling by vector length)

    set_ax_aspect : bool, default: True
        set aspect of matplotlib axes to "equal"

    cmin : float, default: 0.3
        minimal color to use from cmap to avoid pure white

    each_n_points : int, default: 1 [=all]
        show each N points only

    sort_by_length : bool, default: True
        sort vectors by length to avoid clipping (True: Plot longest
        vectors on top)

    override_max_vector_length : bool, default: False
        if True, use 'scale' as absolute scaling. Otherwise, normalize to
        field-vector amplitude.

    Returns
    -------

    return value of matplotlib's `quiver`

    """
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import matplotlib.colors as mcolors
    import numpy as np

    # - prep matplotlib, axes
    ax, show = _get_axis_existing_or_new()
    if cmap is None:
        cmap = cm.Blues
    if set_ax_aspect:
        ax.set_aspect("equal")

    # - to numpy, real part of pos
    _vec = to_np(field_vectors[::each_n_points])
    _pos = to_np(positions[::each_n_points]).real

    # - project on plane
    if projection.lower() == "auto":
        projection = _automatic_projection(_pos)

    vec, pos, levels = _apply_projection_to_vectorfield(
        _vec, _pos, projection, complex_part
    )

    # - optional slicing
    if slice_level is not None:
        slice_level = _get_closest_slice_level(levels, slice_level)
        vec = vec[(levels == slice_level)]
        pos = pos[(levels == slice_level)]

    # - sort and scale by length
    l_vec = np.linalg.norm(vec, axis=1)
    if sort_by_length:
        sort_idx = np.argsort(l_vec)
        pos = pos[sort_idx]
        vec = vec[sort_idx]
        l_vec = l_vec[sort_idx]

    if not override_max_vector_length:
        scale = scale * l_vec.max()
    else:
        scale = scale

    # -- quiver plot
    cscale = mcolors.Normalize(
        l_vec.min() - cmin * (l_vec.max() - l_vec.min()), l_vec.max()
    )  # colors by vector length

    im = ax.quiver(*pos.T, *vec.T, scale=scale, color=cmap(cscale(l_vec)), **kwargs)

    if show:
        plt.show()

    return im


def _streamlines(
    field_vectors,
    positions,
    projection="auto",
    complex_part="real",
    slice_level=None,
    set_ax_aspect=True,
    each_n_points=1,
    density=1,
    start_points="auto",
    broken_streamlines=False,
    **kwargs,
):
    """
    additional kwargs are passed to matplotlib's `streamplot`

    start_points: str
        - 'auto', use matplotlib default.
        - 'top': streamlines calc. starts from top
        - 'bottom', likewise but starting from bottom.
    """
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import matplotlib.colors as mcolors
    import numpy as np

    # - prep matplotlib, axes
    ax, show = _get_axis_existing_or_new()
    if set_ax_aspect:
        ax.set_aspect("equal")

    # - to numpy, real part of pos
    _vec = to_np(field_vectors[::each_n_points])
    _pos = to_np(positions[::each_n_points]).real

    # - project on plane
    if projection.lower() == "auto":
        projection = _automatic_projection(_pos)

    vec, pos, levels = _apply_projection_to_vectorfield(
        _vec, _pos, projection, complex_part
    )

    # - optional slicing
    if slice_level is not None:
        slice_level = _get_closest_slice_level(levels, slice_level)
        vec = vec[(levels == slice_level)]
        pos = pos[(levels == slice_level)]

    # - prepare the data: matplotlib's `streamplot` requires griddata
    v_x, extent, grid_x, grid_z = _interpolate_to_grid(
        pos[:, 0], pos[:, 1], vec[:, 0], return_grid=True
    )
    v_z, extent, grid_x, grid_z = _interpolate_to_grid(
        pos[:, 0], pos[:, 1], vec[:, 1], return_grid=True
    )

    # - optionally: start streamlines specifically from top / bottom
    N_pt_start = density * grid_x.shape[0]
    if start_points.lower() == "top":
        kwargs["start_points"] = np.stack(
            [
                np.linspace(
                    pos[:, 0].min(),
                    pos[:, 0].max(),
                    N_pt_start,
                ),
                np.ones(N_pt_start) * pos[:, 1].max(),
            ]
        ).T
    elif start_points.lower() == "bottom":
        kwargs["start_points"] = np.stack(
            [
                np.linspace(
                    pos[:, 0].min(),
                    pos[:, 0].max(),
                    N_pt_start,
                ),
                np.ones(N_pt_start) * pos[:, 1].min(),
            ]
        ).T

    # - plot
    stplt = plt.streamplot(
        grid_x,
        grid_z,
        v_x[::-1],
        v_z[::-1],
        density=density,
        broken_streamlines=broken_streamlines,
        **kwargs,
    )

    if show:
        plt.show()

    return stplt
