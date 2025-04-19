# encoding=utf-8
"""
3D visualization tools for vector fields
"""
# %%
import warnings

import torch

from torchgdm.constants import COLORS_DEFAULT
from torchgdm.tools.misc import to_np
from torchgdm.tools.misc import get_closest_wavelength
from torchgdm.visu.visu2d._tools import (
    _get_axis_existing_or_new,
    _get_closest_slice_level,
)


def vectorfield(field, illumination_index=0, whichfield="e", **kwargs):
    """plot 3d vectorfield
    
    For doc, see :func:`_vectorfield`
    """
    if whichfield.lower() == "e":
        f = field.efield[illumination_index]
    else:
        f = field.hfield[illumination_index]

    return _vectorfield(f, field.positions, **kwargs)


def vectorfield_inside(sim, wavelength, illumination_index, whichfield="e", **kwargs):
    """plot 3d vectorfield inside structure
    
    For doc, see :func:`_vectorfield`
    """
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
    complex_part="real",
    scale=10.0,
    override_max_vector_length=False,
    cmap="Blues",
    alpha=1,
    show_scalar_bar=False,
    each_n_points=1,
    pl=None,
    show="auto",
    **kwargs,
):
    """plot 2D Vector field as quiver plot

    plot nearfield list as 2D vector plot, using matplotlib's `quiver`.
    `kwargs` are passed to `pyVista.add_mesh`

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

    complex_part : str, default: 'real'
        Which part of complex field to plot. Either 'real' or 'imag'.

    scale : float, default: 10.0
        optional vector length scaling parameter

    cmap : matplotlib colormap, default: `cm.Blues`
        matplotlib colormap to use for arrows (color scaling by vector length)

    alpha : float, default: 1
        opacity of vector arrows

    each_n_points : int, default: 1 [=all]
        show each N points only

    pl : plotter, default: None
        optional pre-existing pyvista plotter to plot into (for composition of scene).

    Returns
    -------

    return value of matplotlib's `quiver`

    """
    try:
        import pyvista as pv
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "`pyvista` not found. Required for 3D plotting. Install with: "
            + "pip install 'jupyterlab>=3' ipywidgets 'pyvista[all,trame]'"
        )
    import numpy as np

    if "projection" in kwargs:
        kwargs.pop("projection")

    # - prep matplotlib, axes
    if type(show) == str:
        if show.lower() == "auto" and pl is None:
            show = True
        else:
            show = False
    if pl is None:
        pl = pv.Plotter()

    # - to numpy, take real or imag part
    f = to_np(field_vectors[::each_n_points])
    p = to_np(positions).real

    if complex_part.lower() == "real":
        f = f.real
    elif complex_part.lower() == "imag":
        f = f.imag
    else:
        raise ValueError(
            "Error: Unknown `complex_part` argument. Must be either 'real' or 'imag'."
        )

    # - vector length for color coding
    l_vec = np.linalg.norm(f, axis=1)

    if not override_max_vector_length:
        scale = scale * l_vec.max()
    else:
        scale = scale

    # - create pyvista data
    pts = pv.PolyData(p)
    pts["length"] = l_vec
    pts.set_active_scalars("length")
    pts["vectors"] = f * scale
    pts.set_active_vectors("vectors")

    # - do the actual plot
    pl.add_mesh(
        pts.arrows,
        cmap=cmap,
        show_edges=False,
        line_width=0.5,
        edge_opacity=alpha,
        opacity=alpha,
        show_scalar_bar=show_scalar_bar,
        name="vectorfield",
        **kwargs,
    )

    if show:
        pl.show()
        pl.camera.azimuth = 180.0  # convention: x-axis to the right

    return pts
